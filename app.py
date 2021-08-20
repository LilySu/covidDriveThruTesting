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
        params = {
            "r": "50",
            "requestType": "dotcom",
            "s": "20",
            "p": 1,
            "q": "78723",
            "lat": "",
            "lng": "",
            "zip": "78723",
        }

        find_locations_api = (
            "https://www.walgreens.com/locator/v1/stores/search?requestor=search"
        )
        find_slots_api = (
            "https://www.walgreens.com/findcarecovidsvc/svc/v2/scheduling/slots?o=acs"
        )
        loc = requests.post(find_locations_api, json=params)

        # store stores and slot times ranked by location
        store_info_ranked_by_location = loc.json()
        store_results = {}
        for idx in range(len(store_info_ranked_by_location["results"])):
            store_dict_and_results = []
            store_number_result = store_info_ranked_by_location["results"][idx][
                "storeNumber"
            ]
            store_number = {"location": str(store_number_result)}
            req = requests.post(find_slots_api, json=store_number)
            store_dict_and_results.append(store_number_result)
            store_dict_and_results.append(req.json())
            key = str(idx)
            store_results[key] = store_dict_and_results
        dbResponse_store = db.store_info.insert_one(
            store_info_ranked_by_location
        )  # created the collection in walgreens
        dbResponse_slot = db.test_timeslots.insert_one(store_results)
        return Response(
            response=json.dumps(
                {
                    "message": "record created",
                    "id_store": f"{dbResponse_store.inserted_id}",
                    "id_slot": f"{dbResponse_slot.inserted_id}",
                }
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
