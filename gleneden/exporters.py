
from scrapy.exporters import BaseItemExporter


import icalendar
import json
from datetime import datetime, date, tzinfo
import pytz
from uuid import uuid5, UUID

from .items import BookableDate

ns = UUID('b1397ae2-6857-11ec-9e5b-6e2c6d516a98')


class ICalItemExporter(BaseItemExporter):
    # similar to the XML exporter
    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.file = file  # already-open file handle

        self.cal = icalendar.Calendar()
        self._kwargs.setdefault('ensure_ascii', not self.encoding)

    def start_exporting(self):
        self.cal.add('prodid', '-//GlenEden//verselogic.net//')
        self.cal.add('version', '2.0')

    def export_item(self, item: BookableDate):

        if not item['should_book']:
            return
        e = icalendar.Event()
        e.add('summary', icalendar.vText(f"Avail: {item['available']}"))

        e.add('location', item['url'])
        
        e.add('uid', icalendar.vText(uuid5(ns, str(item['date']))))

        desc = f"Status: {item['status']}\nBook: {item['should_book']}\n\nPass: \n"
        e.add('description', icalendar.vText(desc))

        e.add('dtstart', item['date'])

        self.cal.add_component(e)


    def finish_exporting(self):
        self.file.write(self.cal.to_ical())
