DROP TABLE if exists mdab;
CREATE TABLE mdab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import mdab_input.txt mdab
create index datum on mdab(id);
pragma table_info (mdab);
select count(*) from mdab;
.exit
