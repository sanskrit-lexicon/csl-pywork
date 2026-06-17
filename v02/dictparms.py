# coding=utf-8
"""dictparms.py
   Central registry of all Cologne Sanskrit Lexicon dictionaries.
   Imported by generate.py and used as the Mako template context for every
   per-dictionary code generation run.

   alldictparms: dict keyed by lowercase dictionary code (dictlo).
     Each entry has: dictup (uppercase code), dictlo, dictname (full Unicode
     title), and dictversion (used in generated file headers).
   microversion: appended to dictversion in generated output so that minor
     changes can be tracked without bumping the main version number.
     Update this string whenever a cross-dictionary template change is made.
"""
# microversion is appended to dictversion in generated output.
# Change it whenever a cross-dictionary template change is deployed.
microversion = '.002'  # abch 11-19-2023
alldictparms = {
 "gra": {
  "dictup":"GRA",
  "dictlo":"gra",
  "dictname":"Grassman Wörterbuch zum Rig Veda",
  "dictversion":"02",
 },
 "bur": {
  "dictup":"BUR",
  "dictlo":"bur",
  "dictname":"Burnouf Dictionnaire Sanscrit-Français",
  "dictversion":"02",
 },
"cae": {
  "dictup":"CAE",
  "dictlo":"cae",
  "dictname":"Cappeller Sanskrit-English Dictionary",
  "dictversion":"02",
 },
 "stc": {
  "dictup":"STC",
  "dictlo":"stc",
  "dictname":"Stchoupak Dictionnaire Sanscrit-Français",
  "dictversion":"02",
 },
"pwg": {
  "dictup":"PWG",
  "dictlo":"pwg",
  "dictname":"Böhtlingk and Roth Grosses Petersburger Wörterbuch",
  "dictversion":"02",
 },
 "mw": {
  "dictup":"MW",
  "dictlo":"mw",
  "dictname":"Monier-Williams Sanskrit-English Dictionary, 1899",
  "dictversion":"02",
 },
 "skd": {
  "dictup":"SKD",
  "dictlo":"skd",
  "dictname":"Sabda-kalpadruma",
  "dictversion":"02",
 },
 "ae": {
  "dictup":"AE",
  "dictlo":"ae",
  "dictname":"Apte Student's English-Sanskrit Dictionary",
  "dictversion":"02",
 },
"pw": {
  "dictup":"PW",
  "dictlo":"pw",
  "dictname":"Böhtlingk Sanskrit-Wörterbuch in kürzerer Fassung",
  "dictversion":"02",
 },
"ap90": {
  "dictup":"AP90",
  "dictlo":"ap90",
  "dictname":"Apte Practical Sanskrit-English Dictionary, 1890",
  "dictversion":"02",
 },
"ap": {
  "dictup":"AP",
  "dictlo":"ap",
  "dictname":"Apte Practical Sanskrit-English Dictionary, revised edition, 1957",
  "dictversion":"02",
 },
"pd": {
  "dictup":"PD",
  "dictlo":"pd",
  "dictname":"An Encyclopedic Dictionary of Sanskrit on Historical Principles",
  "dictversion":"02",
 },
"bhs": {
  "dictup":"BHS",
  "dictlo":"bhs",
  "dictname":"Edgerton Buddhist Hybrid Sanskrit Dictionary",
  "dictversion":"02",
 },
"wil": {
  "dictup":"WIL",
  "dictlo":"wil",
  "dictname":"Wilson Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"yat": {
  "dictup":"YAT",
  "dictlo":"yat",
  "dictname":"Yates Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"shs": {
  "dictup":"SHS",
  "dictlo":"shs",
  "dictname":"Shabda-Sagara Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"gst": {
  "dictup":"GST",
  "dictlo":"gst",
  "dictname":"Goldstücker Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"vcp": {
  "dictup":"VCP",
  "dictlo":"vcp",
  "dictname":"Vacaspatyam",
  "dictversion":"02",
 },
"ben": {
  "dictup":"BEN",
  "dictlo":"ben",
  "dictname":"Benfey Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"bop": {
  "dictup":"BOP",
  "dictlo":"bop",
  "dictname":"Bopp Glossarium Sanscritum",
  "dictversion":"02",
 },
"bor": {
  "dictup":"BOR",
  "dictlo":"bor",
  "dictname":"Borooah English-Sanskrit Dictionary",
  "dictversion":"02",
 },
"ccs": {
  "dictup":"CCS",
  "dictlo":"ccs",
  "dictname":"Cappeller Sanskrit Wörterbuch",
  "dictversion":"02",
 },
"md": {
  "dictup":"MD",
  "dictlo":"md",
  "dictname":"Macdonell Sanskrit-English Dictionary",
  "dictversion":"02",
 },
"mwe": {
  "dictup":"MWE",
  "dictlo":"mwe",
  "dictname":"Monier-Williams English-Sanskrit Dictionary",
  "dictversion":"02",
 },
"mw72": {
  "dictup":"MW72",
  "dictlo":"mw72",
  "dictname":"Monier-Williams Sanskrit-English Dictionary, 1872",
  "dictversion":"02",
 },
"ieg": {
  "dictup":"IEG",
  "dictlo":"ieg",
  "dictname":"Indian Epigraphical Glossary",
  "dictversion":"02",
 },
"inm": {
  "dictup":"INM",
  "dictlo":"inm",
  "dictname":"Index to the Names in the Mahabharata",
  "dictversion":"02",
 },
"krm": {
  "dictup":"KRM",
  "dictlo":"krm",
  "dictname":"Kṛdantarūpamālā",
  "dictversion":"02",
 },
"mci": {
  "dictup":"MCI",
  "dictlo":"mci",
  "dictname":"Mehendale Mahabharata Cultural Index",
  "dictversion":"02",
 },
"pe": {
  "dictup":"PE",
  "dictlo":"pe",
  "dictname":"Puranic Encyclopedia",
  "dictversion":"02",
 },
"pgn": {
  "dictup":"PGN",
  "dictlo":"pgn",
  "dictname":"Personal and Geographical Names in the Gupta Inscriptions",
  "dictversion":"02",
 },
"pui": {
  "dictup":"PUI",
  "dictlo":"pui",
  "dictname":"The Purana Index",
  "dictversion":"02",
 },
"sch": {
  "dictup":"SCH",
  "dictlo":"sch",
  "dictname":"Schmidt Nachträge zum Sanskrit-Wörterbuch",
  "dictversion":"02",
 },
"snp": {
  "dictup":"SNP",
  "dictlo":"snp",
  "dictname":"Meulenbeld Sanskrit Names of Plants",
  "dictversion":"02",
 },
"vei": {
  "dictup":"VEI",
  "dictlo":"vei",
  "dictname":"The Vedic Index of Names and Subjects",
  "dictversion":"02",
 },
"acc": {
  "dictup":"ACC",
  "dictlo":"acc",
  "dictname":"Aufrecht Catalogus Catalogorum",
  "dictversion":"02",
 },
"lan": {
  "dictup":"LAN",
  "dictlo":"lan",
  "dictname":"Lanman Sanskrit Reader Vocabulary",
  "dictversion":"02",
 },
"armh": {
  "dictup":"ARMH",
  "dictlo":"armh",
  "dictname":"Abhidhānaratnamālā of Halāyudha",
  "dictversion":"02",
 },
"pwkvn": {
  "dictup":"PWKVN",
  "dictlo":"pwkvn",
  "dictname":"Böhtlingk Sanskrit-Wörterbuch in kürzerer Fassung, Nachträge und Verbesserungen",
  "dictversion":"02",
 },
"lrv": {
  "dictup":"LRV",
  "dictlo":"lrv",
  "dictname":"Vaidya Standard Sanskrit-English Dictionary",
  "dictversion":"02",
 },
 "abch": {
  "dictup":"ABCH",
  "dictlo":"abch",
  "dictname":"Abhidhānacintāmaṇi of Hemacandrācārya",
  "dictversion":"03",
 },
 "acph": {
  "dictup":"ACPH",
  "dictlo":"acph",
  "dictname":"Abhidhānacintāmaṇipariśiṣṭa of Hemacandrācārya",
  "dictversion":"03",
 },
 "acsj": {
  "dictup":"ACSJ",
  "dictlo":"acsj",
  "dictname":"Abhidhānacintāmaṇiśiloñcha of Jinadeva",
  "dictversion":"03",
 },
 "fri": {
  "dictup":"FRI",
  "dictlo":"fri",
  "dictname":"Frisch Sanskrit Reader Vocabulary, 1956",
  "dictversion":"02",
 },
  "nmmb": {
   "dictup":"NMMB",
   "dictlo":"nmmb",
   "dictname":"Nāmamālikā of Bhoja, 1955",
   "dictversion":"03",
  },
}
