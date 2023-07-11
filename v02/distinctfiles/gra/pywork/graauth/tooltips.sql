DROP TABLE if exists graauthtooltips;
CREATE TABLE graauthtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt graauthtooltips
pragma table_info (graauthtooltips);
select count(*) from graauthtooltips;
.exit
