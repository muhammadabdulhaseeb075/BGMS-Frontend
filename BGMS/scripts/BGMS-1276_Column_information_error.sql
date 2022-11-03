-- Fix information error
--Change consecrated ground to Grave Location in column 6
UPDATE pershore.dataentry_columnposition
set column_id = '372c7df0-49f2-48ff-8993-04c4f97ebbdf'
WHERE template_id = 'ed7e5e27-8bae-454b-be76-1acc621ba722'
	and position = 6

-- Change Grave Location to Grave Number in column 7
UPDATE pershore.dataentry_columnposition
set column_id = 'f49240a3-8742-402a-bd57-d3a153145e27'
WHERE template_id = 'ed7e5e27-8bae-454b-be76-1acc621ba722'
	and position = 7

-- Change Grave Number to Other comments (burial_remarks) in column 8
UPDATE pershore.dataentry_columnposition
set column_id = 'cf429043-3134-4540-bcc3-0cde233dfb47'
WHERE template_id = 'ed7e5e27-8bae-454b-be76-1acc621ba722'
	and position = 8