def initial_event_categories(apps, schema_editor):
    
    EventCategory = apps.get_model('cemeteryadmin', 'EventCategory')
    EventCategory.objects.create(name="Funeral", booking_buffer_duration=30, simultaneous_bookings=1, max_booking_per_day=2)
    EventCategory.objects.create(name="Digging")