TIME_REGEX = r'^\d{1,2}\:\d{2}\s?(AM|PM)$'


def is_numeric(n):
    try:
        float(n)
    except ValueError:
        return False
    return True
