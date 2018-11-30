from pathlib import Path
from requests import get
from lxml import html


class ProductsPage:
    def __init__(self, opts):
        self.aws_url = opts['aws_url']
        self.products_url = self.aws_url + opts['products_page']
        self.use_cached_content = opts.get('use_cached_content', False)
        self.cache_location = Path('.products_page_cache.html')

    def url_content(self):
        return get(self.products_url).content

    def get_page_text(self):
        if self.use_cached_content:
            if self.cache_location.exists():
                return self.cache_location.read_text()
        if self.use_cached_content:
            return self.save_page_to_cache()
        return self.url_content()

    def save_page_to_cache(self):
        page_contents = self.url_content()
        self.cache_location.write_bytes(page_contents)
        return page_contents

    def parse_products_page(self):
        html_obj = html.fromstring(self.get_page_text())
        output = {}
        # Parse the sections for each category
        sections = html_obj.xpath('//*[contains(@class, "lb-item-wrapper")]')
        for section in sections:
            category = section.find('a/span').text
            # print(category)
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
                # print(output[category][service])
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
    products_page = ProductsPage({
        'aws_url': aws_url,
        'products_page': '/products',
        'use_cached_content': True
    })
    output_dict = products_page.parse_products_page()

    # Print output
    print(",".join(list(map(lambda x: '"' + x + '"', headings))))
    for category in output_dict:
        for svc in sorted(output_dict[category].keys()):
            print(join_quoted_values(headings, output_dict[category][svc]))


if __name__ == '__main__':
    main()
