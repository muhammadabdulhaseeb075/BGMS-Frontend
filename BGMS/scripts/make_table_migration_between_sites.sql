/** Migration process **/

SET search_path = 'kirkburton';
SHOW search_path;

/** CREATE TEMPORAL TABLES WITH THE BGSITE_OFFICIAL STRUCTURE **/
CREATE TEMP TABLE temporary_bg_official AS
SELECT * FROM bgsite_official LIMIT 0;

CREATE TEMP TABLE production_temporary_bg_official AS
SELECT * FROM bgsite_official LIMIT 0;

/** COPY THE INFORMATION FROM THE CSV FILES INTO THE BGSITE_OFFICIAL TABLES **/

COPY temporary_bg_official FROM 'C:\Users\User\Desktop\temporary2\staging.bgsite_official.csv'
DELIMITER ',' CSV;
COPY production_temporary_bg_official FROM 'C:\Users\User\Desktop\temporary2\production.bgsite_official.csv'
DELIMITER ',' CSV;

/** SHOW DIFFERENCES STAGGING VS PRODUCTION BGSITE_OFFICIAL **/
SELECT *
FROM temporary_bg_official
EXCEPT
SELECT *
FROM production_temporary_bg_official;

/** CREATE TEMP DATABASES **/
CREATE TEMP TABLE production_temporary_bg_burial_official AS
SELECT * FROM bgsite_burial_official LIMIT 0;

CREATE TEMP TABLE temporary_bg_burial_official AS
SELECT * FROM bgsite_burial_official LIMIT 0;

/** COPY INFORMATION FROM CSV TO TEMPORAL TABLES **/
COPY temporary_bg_burial_official FROM 'C:\Users\User\Desktop\temporary2\staging.bgsite_burial_official.csv'
DELIMITER ',' CSV;
COPY production_temporary_bg_burial_official FROM 'C:\Users\User\Desktop\temporary2\production.bgsite_burial_official.csv'
DELIMITER ',' CSV;

/** DIFFERENCE STAGGING VS PRODUCTION BGSITE_BURIAL_OFFICIAL **/
SELECT *
FROM temporary_bg_burial_official
EXCEPT
SELECT *
FROM production_temporary_bg_burial_official;

/** CREATE INTERSECTION TABLE TO BE EXPORTED FOR BGSITE_OFFICIAL**/
CREATE TABLE temporary_intersection_bg_official AS SELECT *
FROM temporary_bg_official
EXCEPT
SELECT *
FROM production_temporary_bg_official;

/** CREATE INTERSECTION TABLE TO BE EXPORTED FOR BURIAL OFFICIAL**/
CREATE TABLE temporary_intersection_bg_burial_official AS SELECT *
FROM temporary_bg_burial_official
EXCEPT
SELECT *
FROM production_temporary_bg_burial_official;

INSERT INTO bgsite_official
SELECT * FROM temporary_intersection_bg_official;

INSERT INTO bgsite_burial_official
SELECT * FROM temporary_intersection_bg_burial_official;

/** CLEAN UP PROCESS **/

DROP TABLE temporary_intersection_bg_official;
DROP TABLE temporary_intersection_bg_burial_official;

/** Production Script **/

SELECT * FROM bgsite_burial_official;
SELECT * FROM bgsite_official;

/** STEP 1 Create temporal tables **/

CREATE TEMP TABLE temporary_bg_official AS
SELECT * FROM bgsite_official LIMIT 0;

CREATE TEMP TABLE temporary_bg_burial_official AS
SELECT * FROM bgsite_burial_official LIMIT 0;

/** STEP 2 Load information from CSV's, remember to check permissions, and update the dir name of the files **/

COPY temporary_bg_official FROM 'C:\Users\User\Desktop\temporary2\staging.bgsite_official.csv'
DELIMITER ',' CSV;

COPY temporary_bg_burial_official FROM 'C:\Users\User\Desktop\temporary2\staging.bgsite_burial_official.csv'
DELIMITER ',' CSV;

/** STEP 3 Comparate with production tables. **/

/** SHOW NUMBER OF RECORD SHOULD BE THE SAME IN BOTH TABLES  **/
SELECT *
FROM bgsite_official WHERE id IN (SELECT id FROM temporary_bg_official);

/** SHOW NUMBER OF RECORD SHOULD BE THE SAME IN BOTH TABLES  **/
SELECT *
FROM bgsite_burial_official WHERE id IN (SELECT id FROM temporary_bg_burial_official);