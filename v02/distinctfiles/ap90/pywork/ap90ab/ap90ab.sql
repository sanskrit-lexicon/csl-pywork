DROP TABLE if exists ap90ab;
CREATE TABLE ap90ab (
 `id` VARCHAR(100)  UNIQUE,
 `data` TEXT  NOT NULL
);
.separator "\t"
.import ap90ab_input.txt ap90ab
create index datum on ap90ab(id);
pragma table_info (ap90ab);
select count(*) from ap90ab;
.exit
