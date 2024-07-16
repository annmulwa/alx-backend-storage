#!/usr/bin/env python3
""" MongoDB Operations with Python using pymongo """
from pymongo import MongoClient

if __name__ == "__main__":
    """ Provides some stats about Nginx logs stored in MongoDB """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Count total logs
    n_logs = nginx_collection.count_documents({})
    print(f'{n_logs} logs')

    # Count logs by HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')

    # Count status check logs
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f'{status_check} status check')

    # Find top 10 IPs by request count
    top_ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "ip": "$_id", "count": 1}}
    ])

    print("IPs:")
    for top_ip in top_ips:
        ip = top_ip.get("ip")
        count = top_ip.get("count")
        print(f'\t{ip}: {count}')
