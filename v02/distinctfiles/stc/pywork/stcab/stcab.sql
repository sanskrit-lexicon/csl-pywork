DROP TABLE if exists stcab;
CREATE TABLE stcab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import stcab_input.txt stcab
create index datum on stcab(id);
pragma table_info (stcab);
select count(*) from stcab;
.exit
