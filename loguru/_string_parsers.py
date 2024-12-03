import datetime
import re

class Frequencies:
    SECOND = datetime.timedelta(seconds=1)
    MINUTE = datetime.timedelta(minutes=1)
    HOUR = datetime.timedelta(hours=1)
    DAY = datetime.timedelta(days=1)
    WEEK = datetime.timedelta(weeks=1)

def parse_size(size):
    if not isinstance(size, str):
        return size

    match = re.match(r"^(\d+(\.\d+)?)\s*([kmgtp]?b)$", size.lower())
    if not match:
        raise ValueError(f"Invalid size: {size}")

    amount, _, unit = match.groups()
    amount = float(amount)

    units = {
        "b": 1,
        "kb": 1024,
        "mb": 1024 ** 2,
        "gb": 1024 ** 3,
        "tb": 1024 ** 4,
        "pb": 1024 ** 5,
    }

    return int(amount * units[unit])

def parse_frequency(frequency):
    if isinstance(frequency, datetime.timedelta):
        return frequency

    if isinstance(frequency, (int, float)):
        return datetime.timedelta(seconds=frequency)

    if not isinstance(frequency, str):
        raise ValueError(f"Invalid frequency: {frequency}")

    match = re.match(r"^(\d+(\.\d+)?)\s*([smhdw])$", frequency.lower())
    if not match:
        raise ValueError(f"Invalid frequency: {frequency}")

    amount, _, unit = match.groups()
    amount = float(amount)

    units = {
        "s": Frequencies.SECOND,
        "m": Frequencies.MINUTE,
        "h": Frequencies.HOUR,
        "d": Frequencies.DAY,
        "w": Frequencies.WEEK,
    }

    return amount * units[unit]

def parse_time(time):
    if isinstance(time, datetime.time):
        return time

    if isinstance(time, str):
        try:
            return datetime.datetime.strptime(time, "%H:%M:%S").time()
        except ValueError:
            try:
                return datetime.datetime.strptime(time, "%H:%M").time()
            except ValueError:
                raise ValueError(f"Invalid time format: {time}")

    raise ValueError(f"Invalid time: {time}")
