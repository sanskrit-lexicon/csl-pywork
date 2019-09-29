DROP TABLE if exists pwgab;
CREATE TABLE pwgab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import pwgab_input.txt pwgab
create index datum on pwgab(id);
pragma table_info (pwgab);
select count(*) from pwgab;
.exit
