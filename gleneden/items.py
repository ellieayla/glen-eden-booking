# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from datetime import date
from dataclasses import dataclass, field
from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst  # provided by scrapy


class BookableDate(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = Field()

    available = Field()

    cars_current = Field()
    cars_max = Field()

    people_current = Field()
    people_max = Field()

    status = Field()  # Closed, Full, etc

    should_book = Field()

    url = Field()
