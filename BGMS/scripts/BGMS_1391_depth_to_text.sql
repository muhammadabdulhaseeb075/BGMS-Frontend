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
        EXECUTE format('UPDATE %I.bgsite_personfield SET type = ''text'', options = '''' WHERE name = ''Depth'' and options like ''%Option 1%'';',
            rec.schema_name);
	END IF;
    END LOOP;
END;
$$
LANGUAGE plpgsql;
