SET search_path = 'schema_name'
SHOW search_path
ALTER TABLE bgsite_graveref ALTER COLUMN grave_number type character varying(50);

CREATE OR REPLACE FUNCTION migrate_situation_into_grave() RETURNS TABLE(id uuid,
		situation character varying(50),
		graveref_id integer) AS $$
DECLARE
    burial_data CURSOR FOR SELECT bg_b.id, bg_b.situation, bg_b.graveref_id FROM bgsite_burial AS bg_b;
	burial_graveref_id integer DEFAULT NULL;
BEGIN
	DROP TABLE IF EXISTS bgsite_burial_temp;
	CREATE TABLE bgsite_burial_temp(
	    id uuid NOT NULL,
		situation character varying(50) COLLATE pg_catalog."default",
		graveref_id integer
	 );

	 FOR burialrecord IN burial_data
	 LOOP
	 	IF burialrecord.graveref_id IS NULL AND NOT burialrecord.situation = '' THEN
			SELECT bg_gref.id INTO burial_graveref_id FROM bgsite_graveref bg_gref WHERE bg_gref.grave_number = burialrecord.situation;
			IF  burial_graveref_id IS NOT NULL THEN
				INSERT INTO bgsite_burial_temp VALUES (burialrecord.id,burialrecord.situation, burial_graveref_id);
		 	ELSE
				INSERT INTO bgsite_graveref VALUES (default,burialrecord.situation, NULL, NULL);
				SELECT bg_gref.id INTO burial_graveref_id FROM bgsite_graveref bg_gref WHERE bg_gref.grave_number = burialrecord.situation;
		 		INSERT INTO bgsite_burial_temp VALUES (burialrecord.id,burialrecord.situation, burial_graveref_id);
			END IF;
			SELECT NULL INTO burial_graveref_id;
	 	END IF;
	 END LOOP;

	 RETURN QUERY SELECT * FROM bgsite_burial_temp;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION update_gravenumber_field_from_burial_temporal() RETURNS VOID AS $$
DECLARE
	 burial_data_temp CURSOR FOR SELECT bg_b_t.id, bg_b_t.situation, bg_b_t.graveref_id FROM bgsite_burial_temp AS bg_b_t;
BEGIN
	 FOR burialrecord IN burial_data_temp
	 LOOP
	 	UPDATE bgsite_burial bg_b SET graveref_id = burialrecord.graveref_id WHERE bg_b.id = burialrecord.id;
	 END LOOP;
	 DROP TABLE bgsite_burial_temp;
END;
$$ LANGUAGE plpgsql;

SELECT migrate_situation_into_grave();
SELECT update_gravenumber_field_from_burial_temporal();
