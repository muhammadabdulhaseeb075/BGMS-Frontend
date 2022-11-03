-- Delete of dupplicated records because exist in data base with .jpg and .JPG
DELETE FROM hepworth.bgsite_thumbnail
	WHERE image_id in (select id from hepworth.bgsite_image WHERE url LIKE '%.JPG');
DELETE FROM hepworth.dataentry_imagehistory
	WHERE image_id in (select id from hepworth.bgsite_image WHERE url LIKE '%.JPG');
DELETE FROM hepworth.bgsite_burial
	WHERE burial_record_image_id in (select id from hepworth.bgsite_image WHERE url LIKE '%.JPG');
DELETE FROM hepworth.bgsite_tag
	WHERE image_id in (select id from hepworth.bgsite_image WHERE url LIKE '%.JPG');
DELETE FROM hepworth.bgsite_image
	WHERE url LIKE '%.JPG';