DROP TABLE if exists apauthtooltips;
CREATE TABLE apauthtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt apauthtooltips
pragma table_info (apauthtooltips);
select count(*) from apauthtooltips;
.exit
