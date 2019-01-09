from flask import Flask, request, abort
from bson.json_util import dumps
from bson.objectid import ObjectId
from model import ReviewModel
from datetime import datetime
import config
import json

app = Flask(__name__)

config.configure()

@app.route("/reviews/<productid>", methods=['POST'])
def post_review(productid):
    data = request.json
    model = ReviewModel()
    data["productId"] = productid
    data["time"] = datetime.utcnow()
    model.data = data
    model.save()
    if len(model.errors) == 0:
        return "OK"
    else:
        abort(500, model.errors)

@app.route("/reviews/<productid>", methods=['GET'])
def getReviews(productid):
    model = ReviewModel()
    if "token" in request.args:
        model.lastId = ObjectId(request.args["token"])

    model.productId = productid
    model.retrieveReviews()

    last = None
    if len(model.reviews) > 0:
        last = model.reviews[-1]
    
    result = { "reviews": model.reviews }
    if last is not None:
        result["token"] = last["_id"]

    return dumps(result)

@app.route("/reviews/<productid>/summary", methods=['GET'])
def getSummary(productid):
    model = ReviewModel()

    model.productId = productid
    model.retrieveSummary()

    return dumps(model.summary)

@app.route("/reviews/<productid>", methods=['PUT'])
def put_review(productid):
    data = request.json
    model = ReviewModel()
    data["productId"] = productid
    data["time"] = datetime.utcnow()
    model.data = data
    model.update()
    if len(model.errors) == 0:
        return "OK"
    else:
        abort(500, model.errors)

