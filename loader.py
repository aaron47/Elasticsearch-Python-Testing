from elasticsearch import Elasticsearch

import csv

es = Elasticsearch(
    hosts=["https://192.168.1.6:9200/"],
    http_auth=("elastic", "9348Xz5io3gb8her9*Xe"),
    verify_certs=False)

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
