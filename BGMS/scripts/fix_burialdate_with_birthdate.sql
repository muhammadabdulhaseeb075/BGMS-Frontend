UPDATE hepworth.bgsite_person B
	SET birth_date = NULL, impossible_date_day = NULL, impossible_date_month = NULL, impossible_date_year = NULL
FROM hepworth.bgsite_burial A
	WHERE A.death_id = B.id and A.burial_date = B.birth_date;

UPDATE Butterleigh.bgsite_person B
	SET birth_date = NULL, impossible_date_day = NULL, impossible_date_month = NULL, impossible_date_year = NULL
FROM Butterleigh.bgsite_burial A
	WHERE A.death_id = B.id and A.burial_date = B.birth_date;

UPDATE Thelwall.bgsite_person B
	SET birth_date = NULL, impossible_date_day = NULL, impossible_date_month = NULL, impossible_date_year = NULL
FROM Thelwall.bgsite_burial A
	WHERE A.death_id = B.id and A.burial_date = B.birth_date;