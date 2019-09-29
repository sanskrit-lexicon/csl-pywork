DROP TABLE if exists burab;
CREATE TABLE burab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import burab_input.txt burab
create index datum on burab(id);
pragma table_info (burab);
select count(*) from burab;
.exit
