# takes seconds as int and returns the time passed since .
def seconds_to_time_unit(seconds):
    for time_unit, divisor in zip(['Year', 'Month', 'Weak', 'Day', 'Hour'],
                                  [31536000, 2592000, 604800, 86400, 3600]):
        divided = seconds // divisor
        if divided:
            return str(divided) + ' ' + time_unit + int(divided != 1) * 's'
    return 'A While'
