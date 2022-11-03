""" Utils functions """

def python_date_to_display_string(date, include_day=False):
    """
    Converts python date to a readable display date
    """

    display_date = ""

    if include_day:
        display_date = date.strftime("%A ")

    display_date += date.strftime("%d").lstrip("0") + date.strftime(" %b %Y")

    return display_date

def python_time_to_display_string(time):
    """
    Converts python time to a readable display time
    """

    return time.strftime("%I:").lstrip("0").replace(" 0", " ") + time.strftime("%M%p").lower()
