"""
Coiled quickstart to run on pull requests as a basic test for the soundness
of the `coiled` default environments.
"""
import os

import coiled
import dask.dataframe as dd
from dask.distributed import Client

SOFTWARE = os.environ["SOFTWARE_ENV"]

cluster = coiled.Cluster(
    software=SOFTWARE,
    n_workers=10,
    backend_options={"spot": False},
)

client = Client(cluster)


df = dd.read_csv(
    "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.csv",
    dtype={
        "payment_type": "UInt8",
        "VendorID": "UInt8",
        "passenger_count": "UInt8",
        "RatecodeID": "UInt8",
    },
    storage_options={"anon": True},
    blocksize="16 MiB",
).persist()

df.groupby("passenger_count").tip_amount.mean().compute()

client.close()
cluster.close()
