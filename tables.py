from pymongo import MongoClient

def mongo_conn():
    client = MongoClient("mongodb+srv://karhtikshetty1:karthiks563@cluster0.u72062k.mongodb.net/labhkari?retryWrites=true&w=majority")
    db = client['dbtesting']
    return db

def create_host_collection():
    db = mongo_conn()
    # MongoDB creates collections automatically when you insert data, no need for CREATE TABLE
    # We can add a unique index on 'hostname' to mimic the primary key constraint
    db.hosts.create_index("hostname", unique=True)

def pop_host_collection():
    db = mongo_conn()
    hosts = [
        {"hostname": "localhost:5500", "description": "third service", "status": True},
        {"hostname": "localhost:5600", "description": "third service", "status": True},
        {"hostname": "localhost:8800", "description": "first service", "status": False},
        {"hostname": "localhost:9900", "description": "second service", "status": False},
        {"hostname": "localhost:7700", "description": "third service", "status": False}
    ]
    try:
        db.hosts.insert_many(hosts, ordered=False)
    except Exception as e:
        print(f"Error inserting documents: {e}")

def get_working_hosts():
    db = mongo_conn()
    query = {"status": "TRUE"}
    results = db.hosts.find(query, {"_id": 0, "hostname": 1})
    hosts = [res['hostname'] for res in results]
    return hosts


def get_all_hosts():
    db = mongo_conn()
    results = db.hosts.find({}, {"_id": 0, "hostname": 1})
    hosts = [res['hostname'] for res in results]
    return hosts

def update_host_status(hostname, status):
    db = mongo_conn()
    query = {"hostname": hostname}
    new_status = {"$set": {"status": status}}
    result = db.hosts.update_one(query, new_status)
    if result.matched_count > 0:
        print(f"Updated status for {hostname} set status={status}")
    else:
        print(f"No host found with hostname: {hostname}")

if __name__ == "__main__":
    # create_host_collection()
    # pop_host_collection()
    print(get_working_hosts())
    # print(get_all_hosts())
