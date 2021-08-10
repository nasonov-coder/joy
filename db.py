import logging
import sys
from couchbase.cluster import Cluster, PasswordAuthenticator, ClusterOptions

logging.basicConfig(stream=sys.stderr, level=logging.FATAL)

# open cluster and authenticate as Cluster Admin
# зайти в консоль - http://116.203.213.167:8091
cluster = Cluster('couchbase://116.203.213.167',
                  ClusterOptions(PasswordAuthenticator('Administrator', 'wefbax-3wyKtu-cecbor')))
bucket = cluster.bucket("joy")
collection = bucket.default_collection()