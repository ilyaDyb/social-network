
from django.utils import timezone


def tools_get_timestamp(timestamp):
    current_time = timezone.now()
    time_difference_in_minutes = (current_time - timestamp).total_seconds() / 60

    if time_difference_in_minutes < 1:
        return f"{int(time_difference_in_minutes * 60)} seconds ago."
    elif time_difference_in_minutes < 60:
        return f"{int(time_difference_in_minutes)} minutes ago."
    elif time_difference_in_minutes < 1440:
        return f"{int(time_difference_in_minutes // 60)} hours ago."
    elif time_difference_in_minutes < 4320:
        return f"{int(time_difference_in_minutes // 1440)} days ago."
    else:
        return timestamp.strftime("%d %B %H:%M")