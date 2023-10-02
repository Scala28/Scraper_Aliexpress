# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
import json
from json.decoder import JSONDecodeError
from itemadapter import ItemAdapter


class AliexpressResponseSetterSpiderMiddleware:
    def process_spider_input(self, response, spider):
        try:
            data = json.loads(response.body)['data']['result']['mods']
        except Exception:
            response.meta['items'] = []
            return None

        print(data)
        if 'itemList' not in data:
            response.meta['items'] = []
            return None

        items = data['itemList']['content']
        products = []
        for item in items:
            product = {
                'productId': item.get('productId', None),
                'title': self.extract_safely(item, ['title', 'displayTitle']),
                'rating': self.extract_safely(item, ['evaluation', 'starRating']),
                'algo_exp_id': self.extract_safely(item, ['trace', 'detailPage', 'algo_exp_id']),
                'sku_id': self.extract_safely(item, ['trace', 'utLogMap', 'sku_id']),
                'originalPrice': self.parse_price(item, ['prices', 'originalPrice', 'formattedPrice']),
                'salePrice': self.parse_price(item, ['prices', 'salePrice', 'formattedPrice']),
                'discount': self.extract_safely(item, ['prices', 'salePrice', 'discount']),
                'taxRate': self.extract_safely(item, ['prices', 'taxRate']),
                'selled': self.extract_safely(item, ['trade', 'tradeDesc']),
                'free_shipping': self.check_shipping(item.get('sellingPoints')),
                'url': None
            }
            product['url'] = self.parse_url(product['productId'])
            products.append(product)

        response.meta['items'] = products
        return None

    def parse_url(self, productId):
        return (
            "https://it.aliexpress.com/item/{}.html?spm=a2g0o.productlist.main.1.32fe7c61LYdZmH&algo_pvid=b6e88387-3373-42c8-9b75-6e5bccbf5e1d&aem_p4p_detail=202309150855562078330784558930003872148&algo_exp_id=b6e88387-3373-42c8-9b75-6e5bccbf5e1d-0&pdp_npi=4%40dis%21EUR%2125."
            "78%2114.71%21%21%2126.79%21%21%40211b619a16947933562014117e12eb%2112000031963664595%21sea%21IT%21"
            "0%21AS&curPageLogUid=r1GobafDnTig&search_p4p_id=202309150855562078330784558930003872148_1").format(
            productId)

    def check_shipping(self, sellingPoints):
        if sellingPoints is None:
            return None

        for sellingPoint in sellingPoints:
            tagText = self.extract_safely(sellingPoint, ['tagContent', 'tagText'])
            if tagText == "Spedizione gratuita":
                return True

        return False

    def parse_price(self, item, path):
        try:
            strPrice = self.extract_safely(item, path).split(" ")[1]
            return float(strPrice.replace(',', '.'))
        except Exception:
            return None

    def extract_safely(self, json_data, path):
        for next in path:
            try:
                json_data = json_data[next]
            except KeyError:
                return None
        return json_data


class AliexpressItemRequestGeneratorSpiderMiddleware:
    def process_spider_output(self, response, result, spider):
        for item in result:
            if "photos" not in item:
                adapter = ItemAdapter(item)
                if adapter.get('url'):
                    yield scrapy.Request(adapter['url'], callback=spider.parse_product,
                                         cb_kwargs=dict(product=item))
            else:
                yield item



class FirstscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FirstscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
