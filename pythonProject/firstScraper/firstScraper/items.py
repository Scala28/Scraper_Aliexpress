# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class AliexpressItem(Item):
    productId = Field()
    title = Field()
    rating = Field()
    algo_exp_id = Field()
    sku_id = Field()
    originalPrice = Field()
    salePrice = Field()
    discount = Field()
    taxRate = Field()
    selled = Field()
    free_shipping = Field()
    url = Field()
    photos = Field()


