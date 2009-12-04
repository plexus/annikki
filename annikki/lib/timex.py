"""
Some helpers to deal with time. At the moment we ignore users
timezones, the plugin and the web app only deal with UTC times.
This will have to be addressed at some point.
"""

import datetime

def datetime_from_str(s):
     # YYYY-MM-DD HH:MM:SS.TTT
     # 01234567890123456789012
     year = int(s[0:4])
     month = int(s[5:7])
     day = int(s[8:10])
     hour = int(s[11:13])
     minute = int(s[14:16])
     microseconds = int(float(s[17:]) * 1000000.0)
     second, microsecond = divmod(microseconds, 1000000)
     return datetime.datetime(year, month, day, hour, minute, second, microsecond)

def datetime_as_str(dtm):
     part1 = dtm.strftime("%Y-%m-%d %H:%M:%S")
     micros = dtm.microsecond
     if not micros:
         return part1
     part2 = (".%06d" % micros).rstrip('0')
     return part1 + part2
