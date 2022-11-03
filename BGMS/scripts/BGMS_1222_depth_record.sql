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
        EXECUTE format('INSERT INTO %I.bgsite_personfield(id, name, type, options, required, is_default, field_form, "order", content)VALUES (uuid_generate_v4(), ''Depth'', ''select'', ''option1'', false, false, ''BurialDetails'', 1, ''depth'');',
            rec.schema_name);
	END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;
