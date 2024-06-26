# templatetags/schedule_extras.py

from django import template

register = template.Library()

DAY_OFF_MAP = {
    1: ['Monday', 'Tuesday'],
    2: ['Tuesday', 'Wednesday'],
    3: ['Wednesday', 'Thursday'],
    4: ['Thursday', 'Friday'],
    5: ['Friday', 'Saturday'],
    6: ['Saturday', 'Sunday'],
    7: ['Sunday', 'Monday'],
}

@register.filter
def is_day_off(day_off, weekday_name):
    days_off = DAY_OFF_MAP.get(day_off, [])
    return weekday_name in days_off

