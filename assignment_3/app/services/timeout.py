from datetime import timedelta, datetime

LOCKOUT_THRESHOLD = 3                     # failed attempts before lockout
LOCKOUT_DURATION = timedelta(minutes=5)

def is_timeout(timestamp, streak):
    last_failed_dt = datetime.fromisoformat(timestamp)
    time_since_last_fail = datetime.now() - last_failed_dt
    return time_since_last_fail < (LOCKOUT_DURATION * streak)

def remaining_minutes(timestamp, streak):
    last_failed_dt = datetime.fromisoformat(timestamp)
    time_since_last_fail = datetime.now() - last_failed_dt
    remaining = (LOCKOUT_DURATION * streak) - time_since_last_fail
    total_seconds = int(remaining.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return minutes

def has_remaining_attempts(fail):
    return fail+1 > LOCKOUT_THRESHOLD

def lockout_duration(lockout_streak):
    if lockout_streak is None:
        return LOCKOUT_DURATION
    return LOCKOUT_DURATION * lockout_streak
