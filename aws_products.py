from lxml import html
from lxml import etree
import requests


def quotes(instr):
    return '"{}"'.format(instr.strip())

header = [ ','.join(["Category","AWS Service","Description","Link"]) ]
output = {}

aws_url = 'https://aws.amazon.com'
page = requests.get(aws_url + '/products')
tree = html.fromstring(page.content)
wrappers = tree.xpath('//div[@class="aws-item-wrapper"]')

for wrapper in wrappers:
  category = quotes(wrapper.find('a/span').text)
  output[category] = {}
  for service in wrapper.findall('div/div/a'):
    service_name = quotes(service.text)
    service_link = quotes(''.join([aws_url,service.get('href')]))
    service_desc = quotes(service.find('span').text)
    output[category][service_name] = ','.join([service_desc,service_link])

print("\n".join(header))
for category in output.keys():
  for service in sorted(output[category].keys()):
    print( ','.join([category,service, output[category][service]]))
