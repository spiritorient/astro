import datetime
import pytz
import swisseph as swe
from timezonefinder import TimezoneFinder

def degrees_to_dms(degrees):
    d = int(degrees)
    m = int((degrees - d) * 60)
    s = (degrees - d - m / 60) * 3600
    return f"{d}° {m}' {s:.2f}\""

def degrees_to_zodiac(degrees):
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
        "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign = signs[int(degrees // 30)]
    position_in_sign = degrees % 30
    return f"{degrees_to_dms(position_in_sign)} {sign}"

def get_timezone(lat, lon):
    tz_finder = TimezoneFinder()
    timezone_str = tz_finder.timezone_at(lat=lat, lng=lon)
    return timezone_str

def calculate_natal_chart(dob, tob, lat, lon):
    try:
        local_dt = datetime.datetime.strptime(f'{dob} {tob}', '%d.%m.%Y %H:%M')
        timezone_str = get_timezone(lat, lon)
        if timezone_str is None:
            raise ValueError("Could not determine timezone for the given location.")

        local_tz = pytz.timezone(timezone_str)
        local_dt = local_tz.localize(local_dt)
        utc_dt = local_dt.astimezone(pytz.utc)
        julian_day = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute / 60.0)
        swe.set_topo(lon, lat, 0)

        bodies = {
            'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY, 'Venus': swe.VENUS,
            'Mars': swe.MARS, 'Jupiter': swe.JUPITER, 'Saturn': swe.SATURN, 'Uranus': swe.URANUS,
            'Neptune': swe.NEPTUNE, 'Pluto': swe.PLUTO,
        }

        positions = {}
        for body, code in bodies.items():
            position, _ = swe.calc_ut(julian_day, code)
            positions[body] = degrees_to_zodiac(position[0])

        return positions
    except Exception as e:
        raise RuntimeError(f"Error calculating natal chart: {e}")