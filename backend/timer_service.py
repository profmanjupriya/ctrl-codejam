import time

from config import TIME_PER_QUESTION

# In-memory exam timer (use Redis or DB in production for multi-process)
_exam_start_time = None


def start_exam():
    global _exam_start_time
    if _exam_start_time is None:
        _exam_start_time = time.time()


def get_start_time():
    return _exam_start_time


def get_remaining():
    if _exam_start_time is None:
        return None
    return max(0, int(TIME_PER_QUESTION - (time.time() - _exam_start_time)))


def get_status():
    return {
        "started": _exam_start_time is not None,
        "remaining": get_remaining(),
        "start_time": _exam_start_time,
    }
