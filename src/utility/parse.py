import math

def to_float(value):
    try:
        x = float(value)
        if math.isnan(x):
            return 0.0
        return x
    except Exception:
        return 0.0

def to_int(value):
    try:
        x = int(value)
        if math.isnan(x):
            return 0
        return x
    except Exception:
        return 0
    
def to_str(value):
    try:
        if value is None or (isinstance(value, float) and math.isnan(value)):
            return ""
        return str(value)
    except Exception:
        return ""
