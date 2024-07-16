#!/usr/bin/env python3
'''
Python script that provides some stats about Nginx logs stored in MongoDB
'''

from pymongo import MongoClient


METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection):
    '''
    Script that provides some stats about Nginx logs stored in MongoDB
    '''
    # Count total logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count logs for each HTTP method
    print("Methods:")
    for method in METHODS:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count status check logs
    status_check = mongo_collection.count_documents({"path": "/status"})
    print(f"{status_check} status check")


if __name__ == "__main__":
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        nginx_collection = client.logs.nginx
        log_stats(nginx_collection)
