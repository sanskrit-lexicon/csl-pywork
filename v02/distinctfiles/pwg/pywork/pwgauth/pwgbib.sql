DROP TABLE if exists pwgbib;
CREATE TABLE pwgbib (
 `id` VARCHAR(100)  UNIQUE,
 `code` TEXT,
 `codecap` TEXT,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwgbib_input.txt pwgbib
create index datum on pwgbib(id);
pragma table_info (pwgbib);
select count(*) from pwgbib;
.exit
