gender = {
    'M': 0,
    'F': 1
}

retirement_reason = {
    'resignation': 0,
    'dismissal': 1,
    'retirement': 2,
    -1: None
}


def none_value(val):
    return None if val == -1 else val
