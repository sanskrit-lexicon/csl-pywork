"""Preprocess Mako template .py files to make them parseable by ruff.

Mako %if/%elif/%else/%endif directives are not valid Python. This script
converts them to valid Python so that static analysis tools can detect
issues in the Python code embedded in Mako templates.

Usage:
    python utilities/preprocess_mako.py <input_file> [output_file]
    
If output_file is omitted, writes to stdout.
"""

import re
import sys


BLOCK_KEYWORDS = {'def', 'class', 'if', 'elif', 'else', 'for', 'while',
                  'try', 'except', 'finally', 'with'}
CONTINUATION_KEYWORDS = {'else', 'elif', 'except', 'finally'}
BLOCK_OPENERS = BLOCK_KEYWORDS - CONTINUATION_KEYWORDS  # {def, class, if, for, while, try, with}


def _opens_python_block(stripped: str) -> bool:
    """Check if a Python line opens a new block (def, class, if, for, etc.)."""
    if not stripped.endswith(':'):
        return False
    if not stripped:
        return False
    first_word = stripped.split()[0].rstrip(':')
    if first_word in BLOCK_KEYWORDS:
        return True
    if first_word == 'async' and len(stripped.split()) > 1:
        return stripped.split()[1] in ('def', 'for', 'with')
    return False


def _first_keyword(stripped: str) -> str:
    return stripped.split()[0].rstrip(':') if stripped else ''


class PyBlockTracker:
    """Tracks Python block indentation for proper re-indentation."""

    def __init__(self, indent_size: int = 4):
        self.indent_size = indent_size
        self.block_body: int | None = None  # expected body indent
        self.continuation_stack: list[int] = []  # header indents for matching else/elif/etc

    def compute_indent(self, stripped: str, orig_indent: int, default_indent: int | None = None) -> int:
        """Compute proper Python indent for a line."""
        fw = _first_keyword(stripped)

        if fw in CONTINUATION_KEYWORDS and self.continuation_stack:
            peek = self.continuation_stack[-1]
            if fw in ('else', 'elif'):
                self.continuation_stack.pop()
            return peek

        if self.block_body is not None:
            return self.block_body

        if default_indent is not None:
            return default_indent
        return orig_indent

    def update(self, stripped: str, output_indent: int):
        """Update tracker state after outputting a line at output_indent."""
        code_part = stripped.split('#')[0].rstrip()
        if _opens_python_block(code_part):
            self.block_body = output_indent + self.indent_size
            fw = _first_keyword(stripped)
            if fw not in CONTINUATION_KEYWORDS:
                self.continuation_stack.append(output_indent)
            elif fw == 'elif':
                self.continuation_stack.append(output_indent)

    def reset(self):
        """Reset state (used when entering/exiting Mako context)."""
        self.block_body = None
        self.continuation_stack = []

    def save_state(self):
        return (self.block_body, list(self.continuation_stack))

    def restore_state(self, state):
        self.block_body, self.continuation_stack = state


def preprocess_mako(content: str, indent_size: int = 4) -> str:
    """Convert Mako % directives to valid Python for linting."""
    lines = content.split('\n')
    result = []

    mako_depth = 0
    # stack of (indent_of_directive, saved_py_state, saved_py_indent, had_body_content)
    mako_stack = []

    tracker = PyBlockTracker(indent_size)
    py_indent = 0

    mako_control_re = re.compile(
        r'^(\s*)%(\s*)(if|elif|else|endif|for|endfor|while|endwhile|try|except|endtry)\b\s*(.*)'
    )

    for line in lines:
        stripped = line.lstrip()
        orig_indent = len(line) - len(stripped)

        m = mako_control_re.match(line)

        if m:
            kw = m.group(3)
            rest = m.group(4).rstrip()

            if kw in ('if', 'for', 'while', 'try'):
                if mako_depth == 0:
                    base = tracker.block_body if tracker.block_body is not None else py_indent
                    saved_state = tracker.save_state()
                    mako_stack.append([base, saved_state, py_indent, False])
                    tracker.reset()
                else:
                    # Nested Mako block: align with current Python block body
                    base = tracker.block_body if tracker.block_body is not None else mako_stack[-1][0] + indent_size
                    mako_stack.append([base, tracker.save_state(), py_indent, False])
                    tracker.reset()
                line_out = ' ' * base + kw + ' ' + rest
                if not rest.endswith(':'):
                    line_out += ':'
                result.append(line_out)
                mako_depth += 1

            elif kw in ('elif',):
                base = mako_stack[-1][0]
                if not mako_stack[-1][3]:
                    result.append(' ' * (base + indent_size) + 'pass')
                mako_stack[-1][3] = False
                line_out = ' ' * base + 'elif ' + rest
                if not rest.endswith(':'):
                    line_out += ':'
                result.append(line_out)

            elif kw in ('else',):
                base = mako_stack[-1][0]
                if not mako_stack[-1][3]:
                    result.append(' ' * (base + indent_size) + 'pass')
                mako_stack[-1][3] = False
                result.append(' ' * base + 'else:')

            elif kw in ('except',):
                base = mako_stack[-1][0]
                line_out = ' ' * base + 'except ' + rest
                if not rest.endswith(':'):
                    line_out += ':'
                result.append(line_out)

            elif kw in ('endif', 'endfor', 'endwhile', 'endtry'):
                if mako_stack:
                    entry = mako_stack.pop()
                    base, saved_state, saved_py_indent, had_body = entry
                else:
                    base = py_indent
                    saved_state = None
                    saved_py_indent = None
                    had_body = True
                mako_depth -= 1
                if mako_depth < 0:
                    mako_depth = 0
                if saved_state is not None:
                    tracker.restore_state(saved_state)
                    if saved_py_indent is not None:
                        py_indent = saved_py_indent
                else:
                    tracker.reset()
                if not had_body:
                    result.append(' ' * (base + indent_size) + 'pass')
                result.append(' ' * base + 'pass')

        else:
            fw = _first_keyword(stripped)

            if mako_depth > 0:
                # Inside a Mako block — track Python structure relative to Mako base
                mako_base = mako_stack[-1][0]
                if stripped and not stripped.startswith('#'):
                    mako_stack[-1][3] = True  # mark has executable body content
                if stripped:
                    output_indent = tracker.compute_indent(stripped, orig_indent, mako_base + indent_size)
                    result.append(' ' * output_indent + stripped)
                    py_indent = output_indent
                    tracker.update(stripped, output_indent)
                else:
                    result.append('')
            else:
                # Outside Mako blocks — track Python structure normally
                if stripped:
                    if fw in CONTINUATION_KEYWORDS and tracker.continuation_stack:
                        output_indent = tracker.compute_indent(stripped, orig_indent)
                    elif tracker.block_body is not None and orig_indent < tracker.block_body:
                        output_indent = tracker.compute_indent(stripped, orig_indent)
                    else:
                        output_indent = orig_indent
                    result.append(' ' * output_indent + stripped)
                    py_indent = output_indent
                    tracker.update(stripped, output_indent)
                else:
                    result.append('')

    return '\n'.join(result)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_path = sys.argv[1]
    with open(input_path, encoding='utf-8') as f:
        content = f.read()

    output = preprocess_mako(content)

    if len(sys.argv) >= 3:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        sys.stdout.write(output)


if __name__ == '__main__':
    main()
