# takes seconds as int and returns the time passed since .
def seconds_to_time_unit(seconds):
    """
    :param seconds: int, total seconds of passed time from a post/comment publication ...
                    ... or user registration.
    :return: str, returns the longest passed time unit like 1 day, 2 weeks, etc.
    """
    for time_unit, divisor in zip(['Year', 'Month', 'Weak', 'Day', 'Hour'],
                                  [31536000, 2592000, 604800, 86400, 3600]):
        divided = seconds // divisor
        if divided:
            return str(divided) + ' ' + time_unit + int(divided != 1) * 's'
    return 'A While'
