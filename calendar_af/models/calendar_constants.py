import pytz
from datetime import datetime

from odoo import _

# TODO: decide if we are dependent on this variable or the imported schedule duration.
# LOCAL_TZ: Local timezone
LOCAL_TZ = "Europe/Stockholm"
# BASE_DURATION: Base duration given by TeleOpti. This is the duration of the calendar.schedule slots in minutes.
BASE_DURATION = 30.0
# BASE_DAY_START, BASE_DAY_STOP: The hours between which we normally accept appointments
BASE_DAY_START = (
    pytz.timezone(LOCAL_TZ)
    .localize(datetime.now().replace(hour=9, minute=0, second=0, microsecond=0))
    .astimezone(pytz.utc)
)
BASE_DAY_STOP = (
    pytz.timezone(LOCAL_TZ)
    .localize(datetime.now().replace(hour=16, minute=0, second=0, microsecond=0))
    .astimezone(pytz.utc)
)
BASE_DAY_LUNCH = (
    pytz.timezone(LOCAL_TZ)
    .localize(datetime.now().replace(hour=11, minute=0, second=0, microsecond=0))
    .astimezone(pytz.utc)
)
# RESERVED_TIMEOUT is the default time before a reservation times out.
RESERVED_TIMEOUT = 300.0

# Termer
# appointment = faktiskt bokat möte
# occasions = bokningsbara tider
# schedule = occasions skapas utifrån informationen schedules
