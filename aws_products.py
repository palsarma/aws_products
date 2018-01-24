from lxml import html
from lxml import etree
import requests


def quotes(instr):
    return '"{}"'.format(instr.strip())

output = [ ','.join(["Category","AWS Service","Description"]) ]

page = requests.get('https://aws.amazon.com/products/')
tree = html.fromstring(page.content)
wrappers = tree.xpath('//div[@class="aws-item-wrapper"]')

for wrapper in wrappers:
  category = quotes(wrapper.find('a/span').text)
  for service in wrapper.findall('div/div/a'):
    service_name = quotes(service.text)
    service_desc = quotes(service.find('span').text)
    output.append(','.join([category,service_name,service_desc]))

print("\n".join(output))