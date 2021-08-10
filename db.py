import logging
import sys
from couchbase.cluster import Cluster, PasswordAuthenticator, ClusterOptions, QueryOptions
from couchbase.n1ql import QueryResult

logging.basicConfig(stream=sys.stderr, level=logging.FATAL)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# open cluster and authenticate as Cluster Admin

# зайти в консоль - http://116.203.213.167:8091
cluster = Cluster('couchbase://116.203.213.167',
                  ClusterOptions(PasswordAuthenticator('Administrator', 'wefbax-3wyKtu-cecbor')))
bucket = cluster.bucket("joy")
collection = bucket.default_collection()


def upsert(type: str, id: str, doc: object):
    collection.upsert(f'{type}@{id}', {'id': id, 'type': "song", 'doc': doc})


def replace(type: str, id: str, doc: object):
    collection.replace(f'{type}@{id}', {'id': id, 'type': "song", 'doc': doc})


def remove(type: str, id: str):
    collection.remove(f'{type}@{id}')


def get(type: str, id: str):
    collection.get(f'{type}@{id}')


class Params:
    dic = {}
    num = 0

    def __call__(self, obj: object):
        self.num += 1
        self.dic[f'p{self.num}'] = obj
        return f'$p{self.num}'


def query(sql: str, params: Params = None) -> QueryResult:
    qo = None
    if params is not None:
        qo = QueryOptions(named_parameters=params.dic)
    return cluster.query(sql, qo)


def create_params() -> Params:
    return Params()

