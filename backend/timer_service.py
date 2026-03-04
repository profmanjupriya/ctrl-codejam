import time

from config import TIME_PER_QUESTION

# In-memory exam timer (use Redis or DB in production for multi-process)
# When running: _exam_end_time = when the exam period ends (absolute timestamp)
# When paused: _exam_end_time = None, _paused_remaining = seconds left
_exam_end_time = None
_paused_remaining = None


def start_exam():
    """Start the exam timer, or resume from pause."""
    global _exam_end_time, _paused_remaining
    if _paused_remaining is not None:
        # Resume from pause
        _exam_end_time = time.time() + _paused_remaining
        _paused_remaining = None
    elif _exam_end_time is None:
        # Start fresh
        _exam_end_time = time.time() + TIME_PER_QUESTION


def pause_exam():
    """Pause the exam timer (remaining time is preserved)."""
    global _exam_end_time, _paused_remaining
    if _exam_end_time is not None:
        _paused_remaining = max(0, _exam_end_time - time.time())
        _exam_end_time = None


def get_start_time():
    """Truthy if exam has been started (running or paused)."""
    return _exam_end_time is not None or _paused_remaining is not None


def get_remaining():
    if _exam_end_time is not None:
        return max(0, int(_exam_end_time - time.time()))
    if _paused_remaining is not None:
        return int(_paused_remaining)
    return None


def is_paused():
    return _paused_remaining is not None


def get_status():
    return {
        "started": get_start_time(),
        "paused": is_paused(),
        "remaining": get_remaining(),
    }
