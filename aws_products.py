#!/usr/bin/env python3
"""
    Prints csv of AWS Products by screen-scraping AWS products page
"""

from requests import get
from lxml import html


class ProductsPage:
    """
        AWS Products Page
    """
    def __init__(self, aws_url, products_page):
        self.aws_url = aws_url
        self.products_url = self.aws_url + products_page

    def products_page_content(self):
        """ http call to products url and return contents"""
        return get(self.products_url).content

    def parse_products_page(self):
        """ parse products page
            return list of products
            each item is a dict """
        html_obj = html.fromstring(self.products_page_content())
        output = []
        # Parse the sections for each category
        sections = html_obj.xpath('//*[contains(@class, "lb-item-wrapper")]')
        for section in sections:
            category = section.find('a/span').text.strip()
            services = []
            # get details for each service in this category
            for svc in section.findall('div/div/a'):
                services.append({
                    'Category':     category,
                    'Service':      svc.text.strip(),
                    'Description':  svc.find('span').text.strip(),
                    'Link':         self.aws_url + svc.get('href').strip()
                })
            output += sorted(services, key=lambda x: x['Service'])
        return output

def main():
    """ main method """
    products_page = ProductsPage(
        aws_url='https://aws.amazon.com',
        products_page='/products'
    )
    products_list = products_page.parse_products_page()

    # Print output
    quotify = lambda x: '"' + x + '"'
    print(','.join(map(quotify, products_list[0].keys())))
    for product in products_list:
        print(','.join(map(quotify, product.values())))

if __name__ == '__main__':
    main()
