-- this is a comment

SELECT `TABLE_SCHEMA`,`TABLE_NAME`,`COLUMN_NAME`,`ORDINAL_POSITION`
FROM `information_schema`.`COLUMNS`
WHERE `TABLE_SCHEMA` = "information_schema" AND `TABLE_NAME` = "COLUMNS"
ORDER BY `ORDINAL_POSITION` ASC
LIMIT 25;


-- START TIME: 2019-01-23T10:31:55.000001
-- END TIME: 2019-01-23T10:31:55.000002
-- DURATION: 0.000001
-- ROWS COUNT: 22
-- RESULT FILE: 2019-01-23T10-31-55_show-columns.csv
