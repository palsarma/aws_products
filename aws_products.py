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

# Get Categories and corresponding data-ids
CATEGORY_IDS = {}
for wrapper in TREE.xpath('//div[@id="aws-nav-flyout-2-products"]'):
    categories = wrapper.findall('div/div/a')
    for category in categories:
        text = quotes(category.text)
        data_link = category.get('data-flyout')
        CATEGORY_IDS[text] = data_link
        # print (text, data_link)

# Parse the sections for each category
for category in CATEGORY_IDS.keys():
    # print(category)
    OUTPUT[category] = {}
    for service in TREE.xpath('//div[@id="' + CATEGORY_IDS[category] + '"]/div/div[@class="aws-link"]/a'):
        if service.find('span') is None:
            continue
        service_name = quotes(service.text)
        service_desc = quotes(service.find('span').text)
        service_link = service.get('href')
        if AWS_URL not in service_link:
            service_link = AWS_URL + service_link
        OUTPUT[category][service_name] = service_desc + ',' + quotes(service_link)
        # print(category, service_name, service_desc, service_link)

# Print output
print("\n".join(HEADER))
for category in OUTPUT:
    for service in sorted(OUTPUT[category].keys()):
        print(','.join([category, service, OUTPUT[category][service]]))
