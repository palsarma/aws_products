from requests import get
from lxml import html
from pathlib import Path

def quotes(instr):
    return '"{}"'.format(instr.strip())

HEADER = [','.join(["Category", "AWS Service", "Description", "Link"])]
OUTPUT = {}

AWS_URL = 'https://aws.amazon.com'
PAGE = get(AWS_URL + '/products')

# Cache it in a local file
# local_cache = Path('localcache.html')
# local_cache.write_bytes(PAGE.content)
# TREE = html.fromstring(local_cache.read_text())

TREE = html.fromstring(PAGE.content)

CATEGORY_IDS = {}

# Parse the sections for each category
for section in TREE.xpath('//*[contains(@class, "lb-item-wrapper")]'):
    category = quotes(section.find('a/span').text)
    # print(category)
    OUTPUT[category] = {}
    for service in section.findall('div/div/a'):
        service_name = quotes(service.text)
        service_desc = quotes(service.find('span').text)
        service_link = AWS_URL + service.get('href')
        OUTPUT[category][service_name] = service_desc + ',' + quotes(service_link)
        # print(category, service_name, service_desc, service_link)

# Print output
print("\n".join(HEADER))
for category in OUTPUT:
    for service in sorted(OUTPUT[category].keys()):
        print(','.join([category, service, OUTPUT[category][service]]))
