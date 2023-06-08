from django import template

register = template.Library()


@register.simple_tag
def render_stops(stops_amount: int) -> str:
    if stops_amount % 10 == 1 and stops_amount % 100 != 11:
        return f"{stops_amount} зупинку"
    elif 2 <= stops_amount % 10 <= 4 and (stops_amount % 100 < 10 or stops_amount % 100 >= 20):
        return f"{stops_amount} зупинки"
    else:
        return f"{stops_amount} зупинок"