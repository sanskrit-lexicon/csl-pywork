DROP TABLE if exists pwbib;
CREATE TABLE pwbib (
 `id` VARCHAR(100)  UNIQUE,
 `code` TEXT,
 `codecap` TEXT,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwbib_input.txt pwbib
create index datum on pwbib(id);
pragma table_info (pwbib);
select count(*) from pwbib;
.exit
