DROP TABLE if exists benauthtooltips;
CREATE TABLE benauthtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt benauthtooltips
pragma table_info (benauthtooltips);
select count(*) from benauthtooltips;
.exit
