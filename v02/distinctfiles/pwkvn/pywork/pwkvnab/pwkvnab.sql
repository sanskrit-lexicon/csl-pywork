DROP TABLE if exists pwkvnab;
CREATE TABLE pwkvnab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwkvnab_input.txt pwkvnab
create index datum on pwkvnab(id);
pragma table_info (pwkvnab);
select count(*) from pwkvnab;
.exit
