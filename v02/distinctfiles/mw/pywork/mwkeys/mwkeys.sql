DROP TABLE if exists mwkeys;
CREATE TABLE mwkeys (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) UNIQUE,
 data TEXT NOT NULL
);
.separator "\t"
.import extract_keys_b.txt mwkeys
create index datum on mwkeys(key);
pragma table_info (mwkeys);
select count(*) from mwkeys;
.exit
