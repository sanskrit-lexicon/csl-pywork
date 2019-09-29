DROP TABLE if exists westmwtab;
CREATE TABLE westmwtab (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) NOT NULL,
 data TEXT NOT NULL
);
.separator "\t"
.import westmwtab_input.txt westmwtab
pragma table_info (westmwtab);
select count(*) from westmwtab;
.exit
