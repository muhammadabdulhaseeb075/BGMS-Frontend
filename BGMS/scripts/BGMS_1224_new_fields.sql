-- If no exist any records in bgsite_personfield
DO
$$
DECLARE
    rec record;
BEGIN
    FOR rec IN
        SELECT schema_name
        FROM public.main_burialgroundsite
    LOOP
	IF rec.schema_name != 'public' THEN
        EXECUTE 'INSERT INTO '|| rec.schema_name ||'.bgsite_personfield(id, name, type, options, required, is_default, field_form, "order", content) VALUES (uuid_generate_v4(), ''Profession'', ''select'', (SELECT string_agg(profession::text, E''\n'') FROM '|| rec.schema_name ||'.bgsite_profession), false, false, ''DeathPersonDetails'', 1, ''profession'');';
		EXECUTE 'INSERT INTO '|| rec.schema_name ||'.bgsite_personfield(id, name, type, options, required, is_default, field_form, "order", content) VALUES (uuid_generate_v4(), ''Religion'', ''select'', (SELECT string_agg(religion::text, E''\n'') FROM '|| rec.schema_name ||'.bgsite_religion), false, false, ''DeathPersonDetails'', 2, ''religion'');';
		EXECUTE 'INSERT INTO '|| rec.schema_name ||'.bgsite_personfield(id, name, type, options, required, is_default, field_form, "order", content) VALUES (uuid_generate_v4(), ''Parish'', ''select'', (SELECT string_agg(parish::text, E''\n'') FROM '|| rec.schema_name ||'.bgsite_parish), false, false, ''DeathPersonDetails'', 3, ''parish'');';
		EXECUTE 'INSERT INTO '|| rec.schema_name ||'.bgsite_personfield(id, name, type, options, required, is_default, field_form, "order", content) VALUES (uuid_generate_v4(), ''Event'', ''select'', (SELECT string_agg(name::text, E''\n'') FROM '|| rec.schema_name ||'.bgsite_event), false, false, ''DeathPersonDetails'', 4, ''event'');';
	END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;
