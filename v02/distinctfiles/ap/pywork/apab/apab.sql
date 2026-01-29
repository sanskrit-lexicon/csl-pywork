DROP TABLE if exists apab;
CREATE TABLE apab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import apab_input.txt apab
create index datum on apab(id);
pragma table_info (apab);
select count(*) from apab;
.exit
