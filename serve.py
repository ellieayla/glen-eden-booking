import icalendar
import json
from datetime import datetime, date, tzinfo
import pytz

def display(cal):
    s = cal.to_ical().decode()
    return s.replace('\r\n', '\n').strip()


if __name__ == '__main__':
    cal = icalendar.Calendar()

    cal.add('prodid', '-//GlenEden//verselogic.net//')
    cal.add('version', '2.0')

    with open('dates.json', 'r') as f:
        all_loaded_dates = json.load(f)

    for d in all_loaded_dates:
        print(d)

        e = icalendar.Event()
        e.add('summary', 'Python meeting about calendaring')

        event_date = date.fromisoformat(d['date'])
        #event_date.replace(tzinfo=pytz)

        e.add('dtstart', event_date)

        cal.add_component(e)

    print(display(cal))

    with open('dates.ics', 'wb') as f:
        f.write(cal.to_ical())
