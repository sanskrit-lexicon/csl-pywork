DROP TABLE ${dictlo};
CREATE TABLE ${dictlo} (
 key VARCHAR(100)  NOT NULL,
 lnum DECIMAL(10,2) UNIQUE,
 data TEXT NOT NULL
);
.separator "\t"
.import input.txt ${dictlo}
create index datum on ${dictlo}(key);
pragma table_info (${dictlo});
select count(*) from ${dictlo};
.exit
