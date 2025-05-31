from datetime import timedelta


__all__ = [
    "beat_schedule",
]

beat_schedule = {
    "send-messages-every-30-seconds": {
        "task": "send_delayed_messages",
        "schedule": timedelta(seconds=30),
    },
}
