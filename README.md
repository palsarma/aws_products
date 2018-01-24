# aws_products
Script to retrieve the list of AWS Services and their one-line description.

Screen scrapes the url: https://aws.amazon.com/products/

Produces a CSV file containing: Category, Name, Description for each AWS Service found on the page.

Tested under python3 with additional libraries: lxml, requests

## Running
```
python3 aws_products.py > aws_products.csv
```

Sample formatted file: [AWS_Products.xlsx](AWS_Products.xlsx)