import csv
from lxml import html
from web import get_web_page
from selenium.webdriver.common.by import By

class OlxParser:

    def __init__(self):
        self.start_url = 'https://www.olx.ua/'
        self.category_xpath = '//li/a[@data-id]/@href'
        self.proxies = []
        self.agents = []
        self.result_file = 'olx_ads.csv'

        self.fieldnames = ['ad_title', 'ad_date', 'ad_price',
                           'ad_photo', 'ad_link']
        print('Crawler Initialized')

    def get_category_links(self):
        html_code = get_web_page(self.start_url)
        dom_tree = html.fromstring(html_code)
        links = dom_tree.xpath(self.category_xpath)
        print('get_category_links', links)
        return links

    def run(self):
        links = self.get_category_links()

        for link in links:
            html_code = get_web_page(link)
            dom_tree = html.fromstring(html_code)
            self.get_ads(dom_tree)

    def get_ads(self, dom):
        ad_blocks = dom.xpath('//div[@class="offer-wrapper"]')

        with open(self.result_file, 'a') as f:
            csv_writer = csv.DictWriter(f, self.fieldnames)

            for ad in ad_blocks:

                try:

                    ad_title = ad.xpath('.//h3')[0].text_content().strip()
                    ad_date = ad.xpath('.//p[@class="lheight16"]/small[2]')[0].text_content().strip()
                    ad_price = ad.xpath('.//p[@class="price"]')[0].text_content().strip()
                    ad_photo = ad.xpath('.//img/@src')[0]
                    ad_link = ad.xpath('.//h3/a/@href')[0]

                    ad = {
                        'ad_title': ad_title,
                        'ad_date': ad_date,
                        'ad_price': ad_price,
                        'ad_photo': ad_photo,
                        'ad_link': ad_link
                    }

                    csv_writer.writerow(ad)

                    print(ad_title)

                except KeyboardInterrupt:
                    quit()

                except Exception:
                    pass


if __name__ == '__main__':
    olx = OlxParser()
    olx.run()
