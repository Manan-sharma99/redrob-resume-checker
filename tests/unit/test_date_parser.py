from datetime import date, datetime
from typing import Any

def _parse_date(value: Any, default_present: date | None = None) -> date | None:
    if not value:
        return None
    val_str = str(value).strip()
    if not val_str:
        return None
        
    val_lower = val_str.lower()
    if val_lower in ("present", "current", "ongoing"):
        return default_present

    # Extract just the date-like part if it contains time
    # This handles "2020-05-01T00:00:00Z"
    val_str = val_str[:10]
    
    try:
        # YYYY-MM-DD
        if len(val_str) == 10 and val_str[4] == '-' and val_str[7] == '-':
            return datetime.strptime(val_str, "%Y-%m-%d").date()
        # YYYY-MM
        elif len(val_str) >= 7 and val_str[4] == '-':
            return datetime.strptime(val_str[:7], "%Y-%m").date()
        # YYYY
        elif len(val_str) >= 4 and val_str[:4].isdigit():
            return datetime.strptime(val_str[:4], "%Y").date()
    except ValueError:
        pass
    return None

def test():
    as_of = date(2026, 6, 24)
    cases = [
        ("2024-05-15", date(2024, 5, 15)),
        ("2024-05", date(2024, 5, 1)),
        ("2024", date(2024, 1, 1)),
        ("Present", date(2026, 6, 24)),
        ("current", date(2026, 6, 24)),
        ("ONgoing", date(2026, 6, 24)),
        ("2024-05-15T12:00", date(2024, 5, 15)),
        (None, None),
        ("", None),
        ("Invalid", None)
    ]
    for inp, expected in cases:
        res = _parse_date(inp, as_of)
        assert res == expected, f"Failed for {inp}: {res} != {expected}"
    print("All tests passed.")

if __name__ == "__main__":
    test()
