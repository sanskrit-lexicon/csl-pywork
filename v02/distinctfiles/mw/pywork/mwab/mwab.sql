DROP TABLE if exists mwab;
CREATE TABLE mwab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import mwab_input.txt mwab
create index datum on mwab(id);
pragma table_info (mwab);
select count(*) from mwab;
.exit
