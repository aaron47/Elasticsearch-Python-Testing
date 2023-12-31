from elasticsearch import Elasticsearch

import csv
import config

es = Elasticsearch(
    hosts=config.HOSTS,
    http_auth=config.HTTP_AUTH,
    ca_certs=config.CA_CERTS,
    verify_certs=config.VERIFY_CERTS)


print(f"Connected successfully to ElasticSearch cluster `{es.info().body['cluster_name']}`")

with open("./Car details v3.csv", "r") as f:
    reader = csv.reader(f)

    for i, line in enumerate(reader):
        document = {
            "name": line[0],
            "engine": line[9],
            "year": line[1],
            "price": line[2]
        }
        es.index(index="cars", document=document)
