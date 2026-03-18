from datetime import datetime, timedelta
import itertools

def get_previous_day(ts, frmt_in="%Y-%m-%d %H:%M:%S", frmt_out="%Y-%m-%d 00:00:00"):
    """Calcula la fecha del día anterior a partir de un timestamp."""
    return (datetime.strptime(ts, frmt_in) - timedelta(days=1)).strftime(frmt_out)

def unix_to_utc_string(unix_timestamp):
    """Convierte timestamp Unix a string UTC."""
    return datetime.utcfromtimestamp(unix_timestamp).strftime("%Y-%m-%d %H:%M:%S")

def pairwise(iterable):
    """Genera pares consecutivos de elementos de un iterable."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
