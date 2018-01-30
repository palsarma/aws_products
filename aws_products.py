from requests import get
from lxml import html


def quotes(instr):
    return '"{}"'.format(instr.strip())

HEADER = [','.join(["Category", "AWS Service", "Description", "Link"])]
OUTPUT = {}

AWS_URL = 'https://aws.amazon.com'
PAGE = get(AWS_URL + '/products')
TREE = html.fromstring(PAGE.content)
WRAPPERS = TREE.xpath('//div[@class="aws-item-wrapper"]')

for wrapper in WRAPPERS:
    category = quotes(wrapper.find('a/span').text)
    OUTPUT[category] = {}
    for service in wrapper.findall('div/div/a'):
        service_name = quotes(service.text)
        service_link = quotes(''.join([AWS_URL, service.get('href')]))
        service_desc = quotes(service.find('span').text)
        OUTPUT[category][service_name] = ','.join([service_desc, service_link])

print("\n".join(HEADER))
for category in OUTPUT:
    for service in sorted(OUTPUT[category].keys()):
        print(','.join([category, service, OUTPUT[category][service]]))
