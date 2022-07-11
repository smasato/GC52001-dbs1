import argparse
import kindle
import pymongo
import json


def create_mongodb_connection():
    with open('config/production.json', 'r') as f:
        config = json.load(f)

    user = config['MONGODB']['USER']
    pwd = config['MONGODB']['PASSWORD']
    host = config['MONGODB']['HOST']
    port = config['MONGODB']['PORT']
    database = config['MONGODB']['DATABASE']

    client = pymongo.MongoClient('mongodb://' + user + ':' + pwd + '@' + host + ':' + str(port))
    db = client[database]

    return db


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('textfile', type=str)
    args = parser.parse_args()

    highlights = kindle.parse(args.textfile)
    db = create_mongodb_connection()

    if 'highlights' in db.list_collection_names():
        db.drop_collection('highlights')
    db.create_collection('highlights')

    db.highlights.bulk_write(
        [pymongo.InsertOne(dict(highlight.__dict__, **{"vote_count": 0})) for highlight in highlights],
        ordered=False
    )
