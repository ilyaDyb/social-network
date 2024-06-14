
from django.utils import timezone


def tools_get_timestamp(timestamp):
    current_time = timezone.now()
    time_difference_in_minutes = (current_time - timestamp).total_seconds() / 60

    if time_difference_in_minutes < 1:
        return f"{int(time_difference_in_minutes * 60)} seconds ago."
    elif time_difference_in_minutes < 60:
        if int(time_difference_in_minutes) == 1:
            return f"{int(time_difference_in_minutes)} minute ago."
        else:
            return f"{int(time_difference_in_minutes)} minutes ago."
    elif time_difference_in_minutes < 1440:
        if int(time_difference_in_minutes // 60) == 1:
            return f"{int(time_difference_in_minutes // 60)} hour ago."
        else:
            return f"{int(time_difference_in_minutes // 60)} hours ago."
    elif time_difference_in_minutes < 4320:
        if int(time_difference_in_minutes // 1440) == 1:
            return f"{int(time_difference_in_minutes // 1440)} day ago."
        else:
            return f"{int(time_difference_in_minutes // 1440)} day ago."
    else:
        return timestamp.strftime("%d %B %H:%M.")
    
def photo_validate(photo):
    index = str(photo).rfind(".")
    
    if str(photo)[index:] not in [".png", ".jpeg", ".jpg", ".webp"]:
        return {"status": False, "message": "Invalid format"}

    if photo.size > 10 * 1024 * 1024:
        return {"status": False, "message": "Your file is too big"}
    
    return {"status": True}