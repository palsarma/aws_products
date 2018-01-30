# aws_products

Script to retrieve the list of AWS Services and their one-line description.

Screen scrapes the url: [https://aws.amazon.com/products/](https://aws.amazon.com/products/)

Produces a CSV file containing: Category, Name, Description and Link for each AWS Service found on the page.

## Python-way

### Prerequisites

* python3
* libraries:
  * lxml
  * requests

## Save to csv file

```bash
python3 aws_products.py > aws_products.csv
```

Sample formatted file: [AWS_Products.xlsx](AWS_Products.xlsx)

## Docker-way

### Prerequisites

* [Docker](https://docs.docker.com/engine/installation/) >= 17.0

### Build

```bash
docker build -t aws-products .
```

### List all services

```bash
docker run aws-products
```

### Save to csv file

```bash
docker run aws-products > aws_products.csv
```

### Search services by keyword

```bash
docker run aws-products | grep -i %keyword%
```

For example:

![docker run aws-products | grep -i notification](http://i.piccy.info/i9/fe583d3096ac62a7171de8f139802ded/1517352250/59341/1217554/Screenshot_from_2018_01_31_00_43_14.png)
