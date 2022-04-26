DROP TABLE if exists pwkvnbib;
CREATE TABLE pwkvnbib (
 `id` VARCHAR(100)  UNIQUE,
 `code` TEXT,
 `codecap` TEXT,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwkvnbib_input.txt pwkvnbib
create index datum on pwkvnbib(id);
pragma table_info (pwkvnbib);
select count(*) from pwkvnbib;
.exit
