DROP TABLE if exists ap90authtooltips;
CREATE TABLE ap90authtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt ap90authtooltips
pragma table_info (ap90authtooltips);
select count(*) from ap90authtooltips;
.exit
