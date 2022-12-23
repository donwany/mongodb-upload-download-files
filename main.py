# pip install pymongo
import os
import gridfs

from pymongo import MongoClient
from config import USERNAME, PASSWORD

URL = "mongodb+srv://{0}:{1}@rest-api-demo.fml5mkt.mongodb.net/?retryWrites=true&w=majority" \
    .format(USERNAME, PASSWORD)


def mongo_conn():
    """create a connection"""
    try:
        conn = MongoClient(URL, port=27017)
        print("Mongodb Connected", conn)
        return conn.Ytube
    except Exception as err:
        print(f"Error in mongodb connection: {err}")


def upload_file(file_loc, file_name, fs):
    """upload file to mongodb"""
    with open(file_loc, 'rb') as file_data:
        data = file_data.read()

    # put file into mongodb
    fs.put(data, filename=file_name)
    print("Upload Complete")


def download_file(download_loc, db, fs, file_name):
    """download file from mongodb"""
    data = db.youtube.files.find_one({"filename": file_name})

    fs_id = data['_id']
    out_data = fs.get(fs_id).read()

    with open(download_loc, 'wb') as output:
        output.write(out_data)

    print("Download Completed!")


if __name__ == '__main__':
    file_name = "91939.pdf"
    file_loc = "/Users/tsiameh/Desktop/Kubernetes/YoutubeDemo/" + file_name
    down_loc = os.path.join(os.getcwd() + "/downloads/", file_name)

    db = mongo_conn()
    fs = gridfs.GridFS(db, collection="youtube")

    # upload file
    upload_file(file_loc=file_loc, file_name=file_name, fs=fs)
    # download file
    download_file(down_loc, db, fs, file_name)
