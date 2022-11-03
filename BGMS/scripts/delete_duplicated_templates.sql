-- First run clean template history of the template
DELETE FROM pershore.dataentry_templatehistory a
WHERE a.template_id
IN (SELECT id FROM pershore.dataentry_template b WHERE b.name = '1908-1928');

-- Second run clean the columns related to the template
DELETE FROM pershore.dataentry_columnposition a
WHERE a.template_id
IN (SELECT id FROM pershore.dataentry_template b WHERE b.name = '1908-1928');

-- Third run delete the template
DELETE FROM pershore.dataentry_template b
WHERE b.name = '1908-1928';
