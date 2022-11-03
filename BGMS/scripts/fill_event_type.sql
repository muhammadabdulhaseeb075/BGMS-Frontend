INSERT INTO pershore.cemeteryadmin_eventtype(
	id, name, default_duration, event_earliest_time_mon, event_latest_time_mon, event_earliest_time_tue, event_latest_time_tue, event_earliest_time_wed, event_latest_time_wed, event_earliest_time_thu, event_latest_time_thu, event_earliest_time_fri, event_latest_time_fri, event_earliest_time_sat, event_latest_time_sat, event_earliest_time_sun, event_latest_time_sun, event_category_id)
	VALUES (1, 'Burial data', 60, '10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00',
			'10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00'
			, 'Funeral');

INSERT INTO pershore.cemeteryadmin_eventtype(
	id, name, default_duration, event_earliest_time_mon, event_latest_time_mon, event_earliest_time_tue, event_latest_time_tue, event_earliest_time_wed, event_latest_time_wed, event_earliest_time_thu, event_latest_time_thu, event_earliest_time_fri, event_latest_time_fri, event_earliest_time_sat, event_latest_time_sat, event_earliest_time_sun, event_latest_time_sun, event_category_id)
	VALUES (2, 'Celebration', 60, '10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00',
			'10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00', '10:00:00', '16:00:00'
			, 'Digging');