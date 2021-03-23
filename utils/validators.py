def is_integer(number):
    try:
        float(number)
    except ValueError:
        return False
    else:
        return float(number).is_integer()
