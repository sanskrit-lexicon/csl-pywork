DROP TABLE if exists graab;
CREATE TABLE graab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import graab_input.txt graab
create index datum on graab(id);
pragma table_info (graab);
select count(*) from graab;
.exit
