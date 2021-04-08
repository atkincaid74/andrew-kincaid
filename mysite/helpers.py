def is_numeric(n):
    try:
        float(n)
    except ValueError:
        return False
    return True
