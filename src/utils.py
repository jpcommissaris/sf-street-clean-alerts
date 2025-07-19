import datetime
from datetime import datetime, time, timedelta
import calendar

# Direction abbreviation mapping
DIRECTION_ABBR = {
    "North": "N",
    "South": "S",
    "East": "E",
    "West": "W",
    "Northeast": "NE",
    "NorthEast": "NE",
    "Northwest": "NW",
    "NorthWest": "NW",
    "Southeast": "SE",
    "SouthEast": "SE",
    "Southwest": "SW",
    "SouthWest": "SW",
}


def abbreviate_direction(direction: str):
    # Match full or camelcase directions, fallback to first letters if not mapped
    direction = direction.strip()
    return DIRECTION_ABBR.get(
        direction, "".join([w[0] for w in direction.split()]).upper()
    )


def format_hour(hour_str):
    # Accepts string like "6", "14", returns "6am", "2pm"
    hour = int(hour_str)
    if hour == 0:
        return "12am"
    elif hour < 12:
        return f"{hour}am"
    elif hour == 12:
        return "12pm"
    else:
        return f"{hour-12}pm"


def find_next_cleaning(zone, current_dt):
    # Map string days to Python weekday (Monday=0)
    day_map = {"Mon": 0, "Tues": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

    # Create a list of cleaning events [(datetime, fromHour, toHour, day)] (flatten data)
    cleaning_events = []
    for day_str, rules in zone.items():
        if day_str in day_map:
            for rule in rules:
                for week_num, active in enumerate(rule["weeks"], 1):
                    if active:
                        cleaning_events.append(
                            {
                                "weekday": day_map[day_str],
                                "from_hour": int(rule["fromHour"]),
                                "to_hour": int(rule["toHour"]),
                                "week_num": week_num,
                                "day_str": day_str,
                            }
                        )

    # Look ahead for next 31 days (handles all possible week cycles)
    soonest_dt = None
    soonest_event = None
    for days_ahead in range(0, 31):
        candidate_date = current_dt + timedelta(days=days_ahead)
        weekday = candidate_date.weekday()
        week_of_month = ((candidate_date.day - 1) // 7) + 1

        for event in cleaning_events:
            if event["weekday"] == weekday and event["week_num"] == week_of_month:
                # Create cleaning datetime for start
                cleaning_end = candidate_date.replace(
                    hour=event["to_hour"], minute=0, second=0, microsecond=0
                )
                if cleaning_end > current_dt:
                    if soonest_dt is None or cleaning_end < soonest_dt:
                        soonest_dt = cleaning_end
                        soonest_event = event

    if soonest_dt and soonest_event:
        return (soonest_dt, soonest_event)

    # Should never occur.
    raise Exception("No cleaning days found for zone?")


def formatted_zone(zone, now: datetime):
    tuple = find_next_cleaning(zone, now)
    dt_end: datetime = tuple[0]
    event: dict = tuple[1]
    dt_start = dt_end.replace(
        hour=event["from_hour"], minute=0, second=0, microsecond=0
    )

    # Formatting
    street = zone.get("corridor", "Unknown St")
    blockside = abbreviate_direction(zone.get("blockside", ""))
    day_str = dt_start.strftime("%A")  # Full weekday name
    date_str = dt_start.strftime("%B %d")  # e.g., July 20
    from_hour = event["from_hour"]
    to_hour = event["to_hour"]

    time_range = f"{format_hour(from_hour)}-{format_hour(to_hour)}"

    days_away = (dt_start.date() - now.date()).days

    if dt_start <= now < dt_end:
        day_text = "NOW!"
    elif days_away == 0:
        day_text = "TODAY!"
    elif days_away == 1:
        day_text = "TOMORROW!"
    else:
        day_text = f"{days_away} DAYS AWAY!"

    # Build string
    output = (
        f"{street} - ({blockside}): {day_str}, {date_str}: {time_range} ({day_text})"
    )
    return output, dt_start
