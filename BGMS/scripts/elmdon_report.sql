SELECT 
Graveref.grave_number,
Graveplot.memorial_comment,
Graveplot.remarks,
Person.first_names,
Person.last_name,
Burial.user_remarks,
Burial.burial_remarks
FROM elmdon.bgsite_burial Burial
INNER JOIN elmdon.bgsite_graveplot Graveplot
ON Burial.graveplot_id = Graveplot.id
INNER JOIN elmdon.bgsite_graveref Graveref
ON Graveplot.graveref_id = Graveref.id
INNER JOIN elmdon.bgsite_person Person
ON Burial.death_id = Person.id
ORDER BY grave_number ASC
