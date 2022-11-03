-- needed just in case that uuid-ossp extension doesn't exist because uuid_generate_v4() need it
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO pershore.bgsite_official
	SELECT DISTINCT ON (first_names, last_name)
    '' as title, concat_ws(' ',NAMES[1], NAMES[2], NAMES[3], NAMES[4], NAMES[5]) as last_name, '' as first_names, CURRENT_TIMESTAMP as used_on, uuid_generate_v4() as id, Null as address_id, Null as email, Null as phone_number, Null as second_phone_number
    FROM pershore.bgsite_burial A, pershore.bgsite_official B, pershore.bgsite_image C, regexp_split_to_array(A.user_remarks, ' ') as NAMES
	WHERE B.last_name != '' and A.user_remarks != '' and A.user_remarks NOT LIKE '%'||B.last_name||'%' and C.id = A.burial_record_image_id and C.url LIKE '%1908-1928_000%';

INSERT INTO pershore.bgsite_burial_official
	SELECT 'Ceremony performed by' as official_type, A.id as burial_id, B.id as official_id , uuid_generate_v4() as id, '3aea5b65-06b6-46c7-bb2d-a8eaa323f0cd' as burrial_official_type_id
	FROM pershore.bgsite_burial A, pershore.bgsite_official B, pershore.bgsite_image C
	WHERE B.last_name != '' and A.user_remarks != '' and A.user_remarks LIKE '%'||B.last_name||'%' and A.user_remarks LIKE '%'||B.first_names||'%' and C.id = A.burial_record_image_id and C.url LIKE '%1908-1928_000%';

UPDATE pershore.bgsite_burial A
SET user_remarks = ''
	FROM (SELECT A.id
		FROM pershore.bgsite_burial A, pershore.bgsite_official B, pershore.bgsite_image C
		WHERE A.user_remarks != '' and A.user_remarks LIKE '%'||B.last_name||'%' and C.id = A.burial_record_image_id and C.url LIKE '%1908-1928_000%') as S
	WHERE A.id = S.id;