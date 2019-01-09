from db import appdb
from bson.objectid import ObjectId

class ReviewDA():
    def save(self, data):
        appdb.reviews.insert_one(data)

    def retrieveReviews(self, productId, lastId=None):
        filter = { "productId": productId }
        if lastId is not None:
            filter["_id"] = { "$gt": lastId }
        result = [d for d in appdb.reviews.find(filter).sort([( "_id", 1 )]).limit(20)]

        return result

    def _retrieveHistogram(self, productId):
        stages = []
        match = { "$match": { "productId": productId }}
        stages.append(match)
        group = { "$group": { "_id": "$score", "reviews": { "$sum": 1 }} }
        stages.append(group)

        return [d for d in appdb.reviews.aggregate(stages)]

    def _retrieveMedian(self, productId):
        stages = []
        match = { "$match": { "productId": productId }}
        stages.append(match)
        group = {
            "$group": {
                "_id": "",
                "count": {
                    "$sum": 1
                },
                "values": {
                    "$push": "$score"
                }
            }
        }
        stages.append(group)
        unwind = {
            "$unwind": "$values"
        }
        stages.append(unwind)
        sort = {
            "$sort": {
                "values": 1
            }
        }
        stages.append(sort)
        project =  {
            "$project": {
                "count": 1,
                "values": 1,
                "midpoint": {
                    "$divide": [
                        "$count",
                        2
                    ]
                }
            }
        }
        stages.append(project)
        project2 = {
            "$project": {
                "count": 1,
                "values": 1,
                "midpoint": 1,
                "high": {
                    "$ceil": "$midpoint"
                },
                "low": {
                    "$floor": "$midpoint"
                }
            }
        }
        stages.append(project2)
        group2 = {
            "$group": {
                "_id": "",
                "values": {
                    "$push": "$values"
                },
                "high": {
                    "$avg": "$high"
                },
                "low": {
                    "$avg": "$low"
                }
            }
        }
        stages.append(group2)
        project3 = {
            "$project": {
                "beginValue": {
                    "$arrayElemAt": ["$values" , "$high"]
                } ,
                "endValue": {
                    "$arrayElemAt": ["$values" , "$low"]
                }
            }
        }
        stages.append(project3)
        project4 = {
            "$project": {
                "median": {
                    "$avg": ["$beginValue" , "$endValue"]
                }
            }
        }
        stages.append(project4)

        return [d for d in appdb.reviews.aggregate(stages)]

    def _retrieveReviewsWithMoreThanOneVersion(self, productId):
        stages = []
        match = { "$match": { "productId": productId }}
        stages.append(match)
        stages.append({ "$unwind": "$versions" })
        stages.append({ "$group": { "_id": "$_id", "count": { "$sum": 1 } }})
        stages.append({ "$match": {"count": { "$gt": 1 }}})

        reviews = [d for d in appdb.reviews.aggregate(stages)]

        result = []
        for r in reviews:
            result.append(appdb.reviews.find({ "_id": r["_id"] }).next())

        return result


    def retrieveSummary(self, productId):
        result = {
            "median": self._retrieveMedian(productId),
            "summary": self._retrieveHistogram(productId),
            "multiversion_reviews": self._retrieveReviewsWithMoreThanOneVersion(productId)
        }
        
        return result

    def update(self, review):
        cprevious = appdb.reviews.find({ "_id": ObjectId(review["_id"]) })

        previous = cprevious.next()

        if "versions" not in previous:
            review["versions"] = []
        else:
            review["versions"] = previous["versions"]
            previous.pop("version")

        review["versions"].append(previous)
        review["_id"] = ObjectId(review["_id"])

        appdb.reviews.update({ "_id": review["_id"] }, review)

