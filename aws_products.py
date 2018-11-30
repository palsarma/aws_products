#!/usr/bin/env python3

from requests import get
from lxml import html


class ProductsPage:
    def __init__(self, aws_url, products_page):
        self.aws_url = aws_url
        self.products_url = self.aws_url + products_page

    def products_page_content(self):
        return get(self.products_url).content

    def parse_products_page(self):
        html_obj = html.fromstring(self.products_page_content())
        output = {}
        # Parse the sections for each category
        sections = html_obj.xpath('//*[contains(@class, "lb-item-wrapper")]')
        for section in sections:
            category = section.find('a/span').text
            output[category] = {}
            # get details for each service in this category
            for svc in section.findall('div/div/a'):
                service = svc.text
                output[category][service] = {
                    'Category': category,
                    'Service': service,
                    'Description': svc.find('span').text,
                    'Link': self.aws_url + svc.get('href')
                }
        return output


def join_quoted_values(headings, dict_item):
    values = []
    for heading in headings:
        # remove blanks before and after, enclose in quotes
        values.append('"' + dict_item[heading].strip() + '"')
    return ','.join(values)


def main():
    aws_url = 'https://aws.amazon.com'
    headings = ["Category", "Service", "Description", "Link"]
    products_page = ProductsPage(
        aws_url=aws_url,
        products_page='/products'
    )
    output_dict = products_page.parse_products_page()

    # Print output
    print(",".join(list(map(lambda x: '"' + x + '"', headings))))
    for category in output_dict:
        for svc in sorted(output_dict[category].keys()):
            print(join_quoted_values(headings, output_dict[category][svc]))


if __name__ == '__main__':
    main()
