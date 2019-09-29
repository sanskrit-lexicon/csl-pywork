DROP TABLE if exists caeab;
CREATE TABLE caeab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import caeab_input.txt caeab
create index datum on caeab(id);
pragma table_info (caeab);
select count(*) from caeab;
.exit
