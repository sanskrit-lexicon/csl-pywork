DROP TABLE if exists lanab;
CREATE TABLE lanab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import lanab_input.txt lanab
create index datum on lanab(id);
pragma table_info (lanab);
select count(*) from lanab;
.exit
