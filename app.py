from flask import Flask, request
from elasticsearch import Elasticsearch

import config

es = Elasticsearch(
    hosts=config.HOSTS,
    http_auth=config.HTTP_AUTH,
    ca_certs=config.CA_CERTS,
    verify_certs=config.VERIFY_CERTS)

print(f"Connected successfully to ElasticSearch cluster `{es.info().body['cluster_name']}`")

app = Flask(__name__)

MAX_SIZE = 15


@app.route('/search')
def search_autocomplete():
    query: str = request.args["q"].lower()
    tokens: list[str] = query.split(" ")

    clauses = [
        {
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "name": {
                            "value": i,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
        }

        for i in tokens
    ]

    payload = {
        "bool": {
            "must": {
                "span_near": {
                    "clauses": clauses,
                    "slop": 0,
                    "in_order": False,
                }
            }
        }
    }

    res = es.search(index="cars", query=payload, size=MAX_SIZE)
    return [result["_source"]["name"] for result in res["hits"]["hits"]]


if __name__ == '__main__':
    app.run()
