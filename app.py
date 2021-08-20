import json

import pymongo
import requests
from flask import Flask, Response, render_template, request

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost", port=27017, serverSelectionTimeoutMS=1000
    )
    db = mongo.walgreens
    mongo.server_info()  # trigger exception if cannot connect to database
except:
    print("Let's try again to connect to the db")


@app.route("/")
def index():
    try:
        store_record = {"name": "A", "lastName": "B"}
        dbResponse = db.store_info.insert_one(
            store_record
        )  # created the collection in walgreens
        # print(dbResponse.inserted_id)
        # for attr in dir(dbResponse):
        #     print(attr)
        return Response(
            response=json.dumps(
                {"message": "record created", "id": f"dbResponse.inserted_id"}
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as ex:
        print(ex)
    # req = requests.post('https://www.walgreens.com/findcarecovidsvc/svc/v2/scheduling/slots?o=acs', json={"location": "10615"})

    # data = json.loads(req.content)
    # return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run(port=80, debug=True)
