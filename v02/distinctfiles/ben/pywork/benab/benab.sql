DROP TABLE if exists benab;
CREATE TABLE benab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import benab_input.txt benab
create index datum on benab(id);
pragma table_info (benab);
select count(*) from benab;
.exit
