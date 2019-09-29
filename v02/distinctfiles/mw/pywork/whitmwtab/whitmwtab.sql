DROP TABLE if exists whitmwtab;
CREATE TABLE whitmwtab (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) NOT NULL,
 data TEXT NOT NULL
);
.separator "\t"
.import whitmwtab_input.txt whitmwtab
pragma table_info (whitmwtab);
select count(*) from whitmwtab;
.exit
