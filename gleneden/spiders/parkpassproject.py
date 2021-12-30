import scrapy

import urllib.parse
from scrapy.item import Item
from scrapy.loader import ItemLoader

from gleneden.items import BookableDate
import json
from datetime import date


class ParkpassprojectSpider(scrapy.Spider):
    name = 'parkpassproject'
    allowed_domains = ['parkpassproject.com']
    start_urls = ['https://book.parkpassproject.com/book?inventoryGroup=1554186518&inventory=1492413597']

    def parse(self, response):
        # https://docs.scrapy.org/en/latest/topics/loaders.html#nested-loaders ?

        data = response.xpath('//script[@id="__NEXT_DATA__"]/text()')[0].get()
        

        content = json.loads(data)

        daily_occupancy = content['props']['initialState']['book']['dailyOccupancy']
        
        
        for k,v in daily_occupancy.items():


            scheme, netloc, path, query_string, fragment = urllib.parse.urlsplit(response.url)

            current_qs = urllib.parse.parse_qs(query_string)
            current_qs['startDate'] = k
            new_query_string = urllib.parse.urlencode(current_qs, doseq=True)
            today_url = urllib.parse.urlunsplit((scheme, netloc, path, new_query_string, fragment))

            available = min([
                v['maxCars'] - v['currentCars'],
                v['maxPeople'] - v['currentPeople']
            ])

            should_book = all([
                available > 0,
                v['status'] not in ('FULL', 'CLOSED'),
            ])
            yield BookableDate(
                date = date.fromisoformat(k),
                cars_current = v['currentCars'],
                cars_max = v['maxCars'],
                people_current = v['currentPeople'],
                people_max = v['maxPeople'],
                status = v['status'],
                should_book = should_book,
                available = available,
                url = today_url,
            )

