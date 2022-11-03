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
        EXECUTE format('INSERT INTO %I.bgsite_personfield( id, name, type, options, required, is_default) VALUES (uuid_generate_v4(), ''Burial Title'', ''text'', '''', false, false);',
            rec.schema_name);
	END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;

-- Fix upper case in title and add Burial in the beginning
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
        EXECUTE format('UPDATE %I.bgsite_personfield SET name=''Burial Title'' WHERE name = ''title'';',
            rec.schema_name);
	END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;