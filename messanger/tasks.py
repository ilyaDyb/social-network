from celery import shared_task
from typing import Any

from messanger.models import Message


@shared_task
def read_last_messages(user_id: Any, chat_id: Any) -> None:
    try:
        Message.objects.filter(chat__id=chat_id, sender_id=user_id).update(is_read=True)
    except Exception:
        return None
    return None