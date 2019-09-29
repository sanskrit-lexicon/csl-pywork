DROP TABLE if exists mwauthtooltips;
CREATE TABLE mwauthtooltips (
 `cid` VARCHAR(20) NOT NULL,
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL,
 `type` VARCHAR(20) NOT NULL
);
.separator "\t"
.import tooltip.txt mwauthtooltips
pragma table_info (mwauthtooltips);
select count(*) from mwauthtooltips;
.exit
