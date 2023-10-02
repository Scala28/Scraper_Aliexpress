import scrapy
from ..items import AliexpressItem
import requests


class Aliexpress(scrapy.Spider):
    name = "aliexpress"
    allowed_domains = ["best.aliexpress.com",
                       "it.aliexpress.com"]
    start_urls = [""]

    def start_requests(self):
        url = "https://www.aliexpress.com/fn/search-pc/index"
        payload = "{\"pageVersion\":\"984c9a58b6d16e5d8c31de9b899f058a\",\"target\":\"root\",\"data\":{\"CatId\":100006206,\"g\":\"y\",\"isCategoryBrowse\":true,\"isrefine\":\"y\",\"page\":7,\"spm\":\"a2g0o.best.107.2.12a35132DpaVry\",\"trafficChannel\":\"af\",\"origin\":\"y\"},\"eventName\":\"onChange\",\"dependency\":[]}"
        for x in range(1, 2):
            headers = {
                'authority': 'www.aliexpress.com',
                'accept': '*/*',
                'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
                'bx-v': '2.5.3',
                'content-type': 'application/json;charset=UTF-8',
                'cookie': 'cna=T+ZvGEqt9RICAV0ufA2Qy3oE; xman_f=x+xSoyw2pEq6b4PVBrJFAfC2qJcEr06YlNyV9ymD8PMUUxX8X1hFdREi/BvmDx2WL2ejqGgpTW73EbSqnBYfXS4P/lat5EAj2kkIWijO/6K2aU/gCt1HVg==; af_ss_a=1; _ym_uid=1664644171937745609; xman_t=yhkq6ku8yPEr30m8GJ5q3QFNPy5WwF0nSppfuA/uC2rzNTNPkCgrMV255AmcytRq; af_ss_b=1; ali_apache_id=33.59.217.127.1690126406206.250458.2; _ga_save=yes; ali_apache_track=; e_id=pt20; _gcl_au=1.1.846063702.1693928225; _fbp=fb.1.1693928225538.240798904; traffic_se_co=%7B%7D; _ym_d=1694182614; aep_usuc_f=site=ita&c_tp=EUR&ups_d=1|1|1|1&ups_u_t=1709734949707&region=IT&b_locale=it_IT&ae_u_p_s=2; acs_usuc_t=x_csrf=in94k3ygd1n_&acs_rt=0a112c6157324baa8ec5628ad1bf422f; intl_locale=it_IT; ali_apache_tracktmp=; g_state={"i_p":1694281900871,"i_l":2}; XSRF-TOKEN=0e4d6237-803c-4fb3-a6ed-8e2f8dd0afe0; _gid=GA1.2.1953609736.1694423158; xlly_s=1; aep_history=keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%091005005683072769%091005003354077188%091005005906066287%091005005271306977%091005002687405633%091005005727877893%091005005619774026%091005005219864671; xman_us_f=x_locale=it_IT&x_l=0&x_c_chg=0&x_c_synced=0&x_as_i=%7B%22aeuCID%22%3A%22e64dd09b3bba4bd8b944debfcc6505b2-1694461636938-04252-_9QQpXy%22%2C%22af%22%3A%221980572%22%2C%22affiliateKey%22%3A%22_9QQpXy%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%221%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%221885425835%22%2C%22tagtime%22%3A1694461636938%7D&acs_rt=4d36e24fb7ea4ce78226e3057cf95b1c; aeu_cid=e64dd09b3bba4bd8b944debfcc6505b2-1694461636938-04252-_9QQpXy; _m_h5_tk=be5642d9ab930460b5c9ef8cd801e6f8_1694532655828; _m_h5_tk_enc=4f122b34d75f53b5a4f552588b591ba4; cto_bundle=_kg2LV8wd0MyYmFMNmtad2xHWExtYk9jT3JtTkRzdzRWMm9Kb291enZ5alVqQkFrWSUyRm1LZU0zaTVJZjJRYThQJTJCbFBsbnI0YUs2S20xSE1DcDNvJTJGdVNVS2slMkZXY1VkSDlLamxUcWJjaWZ0ZWJ3YWdkTEhqVTlIQ2tQR2JubHNaVXlhQnh1SkRYWTdYZFV3cUJnN1ZOY2tadG9uZE01b0hwSzVVa3JORW5QQTdLS1BTSSUzRA; _ym_isad=2; JSESSIONID=5EFEBBA747F9AA168CA3DC7F408C2FE7; intl_common_forever=xNkEmvUXdCG0MQaFlnGs6lBjclE2imFBb+Pju8x3jO9CJ581kB5m6w==; _ga=GA1.1.caea0efe-1364-468b-aa78-4be482af6c32.1690126406651; _ga_VED1YSGNC7=GS1.1.1694530016.12.1.1694531979.56.0.0; RT="z=1&dm=aliexpress.com&si=fac85738-930f-4361-ad64-8f0849e24480&ss=lmgfhng9&sl=0&tt=0&rl=1"; tfstk=dnUwzAYvrNQN8On0m0u4aWRLdlgtJ4B5IrMjiSVm1ADM5F90Y-w31lTjlmY4iSn05VN_LxybZlws5m_0LjGmnx0miDVnavHbfxNgim23EhashAZeg7eEl-PA6jD0n-kbfM_7653xoTwVPaNTw_A_736C_oaYdqX5Fa_OYhUIol674CICFPY9qQipGSM35EIDc4CpA3L2uylF6YNN_eG4yf-tU5keOYacQCvxtWo8klJD0ccKTY1FT5pqVgf..; l=fBjSAFquO8PrffTjBO5BKurza779uBOfl-FzaNbMiIEGC6UdGm9RSU-QVuGl2LtRJWXPMdYH43ticBptNekY8yDfnSI97Ix0Y6JyCe8C582bY; isg=BAkJa9IaiLhdp06k437UFPvjGDVjVv2I_0Qvt6t5kfWi8iME8af3WQFkNU7E0ZXA; aep_usuc_f=site=ita&c_tp=EUR&ups_d=1|1|1|1&ups_u_t=1709734949707&region=IT&b_locale=it_IT&ae_u_p_s=2; intl_common_forever=Jnb746I1YDqWfDKD5AJGIAXSY0GY/dqneDuPeCYCgWSwnlup3td4VQ==; intl_locale=it_IT; xman_us_f=x_locale=it_IT&x_l=0&x_c_chg=0&x_c_synced=0&x_as_i=%7B%22aeuCID%22%3A%22e64dd09b3bba4bd8b944debfcc6505b2-1694461636938-04252-_9QQpXy%22%2C%22af%22%3A%221980572%22%2C%22affiliateKey%22%3A%22_9QQpXy%22%2C%22channel%22%3A%22AFFILIATE%22%2C%22cv%22%3A%221%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%221885425835%22%2C%22tagtime%22%3A1694461636938%7D&acs_rt=4d36e24fb7ea4ce78226e3057cf95b1c',
                'origin': 'https://www.aliexpress.com',
                'referer': 'https://www.aliexpress.com/category/100006206/pet-products.html?CatId=100006206&g=y&isCategoryBrowse=true&isrefine=y&'
                           'page={}&spm=a2g0o.best.107.2.12a35132DpaVry&trafficChannel=af'.format(x),
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
            }
            yield scrapy.Request(url, callback=self.parse, method="POST", headers=headers, body=payload)

    def parse(self, response):
        items = []
        for x in response.meta['items']:
            item = AliexpressItem(x)
            items.append(item)
            yield item

    def parse_product(self, response, product):
        img_container = response.xpath("//*[@id='pdp-main-image']/div/div/div[2]/ul").extract()
        print(response.body)
        product['photos'] = len(img_container)
        yield product
