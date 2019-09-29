DROP TABLE if exists pwab;
CREATE TABLE pwab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwab_input.txt pwab
create index datum on pwab(id);
pragma table_info (pwab);
select count(*) from pwab;
.exit
