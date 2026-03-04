import time

from config import TIME_PER_QUESTION, TIMER_SUSPENDED

# In-memory exam timer (use Redis or DB in production for multi-process)
# When running: _exam_end_time = when the exam period ends (absolute timestamp)
# When paused: _exam_end_time = None, _paused_remaining = seconds left
_exam_end_time = None
_paused_remaining = None


def _suspended():
    """When True, timer is suspended: exam always 'started', no countdown."""
    return TIMER_SUSPENDED


def start_exam():
    """Start the exam timer, or resume from pause. No-op when timer suspended."""
    if _suspended():
        return
    global _exam_end_time, _paused_remaining
    if _paused_remaining is not None:
        # Resume from pause
        _exam_end_time = time.time() + _paused_remaining
        _paused_remaining = None
    elif _exam_end_time is None:
        # Start fresh
        _exam_end_time = time.time() + TIME_PER_QUESTION


def pause_exam():
    """Pause the exam timer (remaining time is preserved). No-op when timer suspended."""
    if _suspended():
        return
    global _exam_end_time, _paused_remaining
    if _exam_end_time is not None:
        _paused_remaining = max(0, _exam_end_time - time.time())
        _exam_end_time = None


def reset_exam():
    """Hard reset: restart full TIME_PER_QUESTION window and clear any pause state. No-op when suspended."""
    if _suspended():
        return
    global _exam_end_time, _paused_remaining
    _exam_end_time = time.time() + TIME_PER_QUESTION
    _paused_remaining = None


def get_start_time():
    """
    Return the exam start timestamp (seconds since epoch) or None.
    When timer is suspended, returns truthy so exam is always "started".
    """
    if _suspended():
        return 1
    if _exam_end_time is not None:
        # When running, infer start time from end time and total duration.
        return _exam_end_time - TIME_PER_QUESTION
    if _paused_remaining is not None:
        # When paused, infer approximate start time based on how much time
        # has already elapsed. This does not need to be exact for clients,
        # they only care that "started" is True.
        elapsed = TIME_PER_QUESTION - _paused_remaining
        return time.time() - elapsed
    return None


def get_remaining():
    if _suspended():
        return None
    if _exam_end_time is not None:
        return max(0, int(_exam_end_time - time.time()))
    if _paused_remaining is not None:
        return int(_paused_remaining)
    return None


def is_paused():
    return not _suspended() and _paused_remaining is not None


def get_status():
    return {
        "started": get_start_time() is not None,
        "paused": is_paused(),
        "remaining": get_remaining(),
        "suspended": _suspended(),
    }
