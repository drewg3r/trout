from datetime import timedelta, datetime

from django import template
from django.utils import formats

register = template.Library()


@register.simple_tag
def timedelta_to_minutes(td: timedelta) -> int:
    """Get amount of minutes from timedelta rounded up"""
    return int(1 + td.total_seconds() / 60)


@register.simple_tag
def render_time(dt: datetime) -> str:
    """Render datetime object to a readable string"""
    if dt.date() == datetime.today().date():
        return dt.strftime('%H:%M')
    return dt.strftime('%d %b at %H:%M')


def render_minutes(minutes: int) -> str:
    if minutes % 10 == 1 and minutes % 100 != 11:
        return f"{minutes} хвилина"
    elif 2 <= minutes % 10 <= 4 and (minutes % 100 < 10 or minutes % 100 >= 20):
        return f"{minutes} хвилини"
    else:
        return f"{minutes} хвилин"

def render_hours(hours: int) -> str:
    if hours % 10 == 1 and hours % 100 != 11:
        return f"{hours} година"
    elif 2 <= hours % 10 <= 4 and (hours % 100 < 10 or hours % 100 >= 20):
        return f"{hours} години"
    else:
        return f"{hours} годин"

@register.simple_tag
def render_timedelta(td: timedelta) -> str:
    hours = timedelta_to_minutes(td) // 60
    minutes = timedelta_to_minutes(td) % 60
    if not hours:
        return f'{render_minutes(minutes)}'
    elif not minutes:
        return f'{render_hours(hours)}'
    return f'{render_hours(hours)}, {render_minutes(minutes)}'
