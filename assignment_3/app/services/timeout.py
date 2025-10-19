from datetime import timedelta, datetime

LOCKOUT_THRESHOLD = 3
LOCKOUT_DURATION = timedelta(minutes=5)

# Check if user is locked out based on lockout timestamp, and number of lockouts in a row
def is_timeout(timestamp, streak):
    last_failed_dt = datetime.fromisoformat(timestamp)
    time_since_last_fail = datetime.now() - last_failed_dt
    return time_since_last_fail < (LOCKOUT_DURATION * streak)

# Remaining minutes of lockout, for display purposes only
def remaining_minutes(timestamp, streak):
    last_failed_dt = datetime.fromisoformat(timestamp)
    time_since_last_fail = datetime.now() - last_failed_dt
    remaining = (LOCKOUT_DURATION * streak) - time_since_last_fail
    total_seconds = int(remaining.total_seconds())
    minutes, seconds = divmod(total_seconds, 60)
    return minutes

# Check if user has more guesses
def has_remaining_attempts(fail):
    return fail+1 > LOCKOUT_THRESHOLD

# How long a lockout should last based on lockouts in a row
def lockout_duration(lockout_streak):
    if lockout_streak is None:
        return LOCKOUT_DURATION
    return LOCKOUT_DURATION * lockout_streak
