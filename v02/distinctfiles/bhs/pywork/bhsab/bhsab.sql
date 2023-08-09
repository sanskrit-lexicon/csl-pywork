DROP TABLE if exists bhsab;
CREATE TABLE bhsab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import bhsab_input.txt bhsab
create index datum on bhsab(id);
pragma table_info (bhsab);
select count(*) from bhsab;
.exit
