DROP TABLE if exists bhsauthtooltips;
CREATE TABLE bhsauthtooltips (
 `key` VARCHAR(20) NOT NULL,
 `data` VARCHAR(20000) NOT NULL
);
.separator "\t"
.import tooltip.txt bhsauthtooltips
pragma table_info (bhsauthtooltips);
select count(*) from bhsauthtooltips;
.exit
