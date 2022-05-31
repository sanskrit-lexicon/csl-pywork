DROP TABLE if exists schauthtooltips;
CREATE TABLE schauthtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt schauthtooltips
pragma table_info (schauthtooltips);
select count(*) from schauthtooltips;
.exit
