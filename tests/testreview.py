import unittest
from model import ReviewModel
from da import ReviewDA
from mock import MagicMock
from bson.objectid import ObjectId

import inject

json_example = {
    "productId": "B001E4KFG0",
    "userId": "A3SGXH7AUHU8GW",
    "profileName": "delmartian",
#    "helpfulness": "1/1 (Fraction of users who found it helpful)",
    "score": 5.0,
    "summary": "Good Quality Dog Food",
    "text": """I have bought several of the Vitality canned dog food products and have
found them all to be of good quality. The product looks more like a stew than
a processed meat and it smells better. My Labrador is finicky and she
appreciates this product better than most."""
}

class TestReview(unittest.TestCase):
    def tryValidData(self, data):
        reviewDAMock = MagicMock()

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()
        model.data = data
        model.save()

        reviewData = {
                "userId": data["userId"],
                "profileName": data["profileName"],
                "score": data["score"],
                "summary": data["summary"],
                "text": data["text"]
                }
        reviewDAMock.save.assert_called_once_with(data["productId"], reviewData)

    def tryMissingData(self, data, expectedErrors):
        reviewDAMock = MagicMock()

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()
        model.data = data
        model.save()

        reviewDAMock.save.assert_not_called()
        self.assertItemsEqual(expectedErrors, model.errors)

    def test_simple_good_json(self):
        self.tryValidData(json_example)

    def test_score_validType(self):
        json = json_example.copy()
        json["score"] = 5

        self.tryValidData(json)

    def test_validate_json_provided(self):
        reviewDAMock = MagicMock()

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()
        model.save()

        reviewDAMock.save.assert_not_called()
        expectedErrors = ['json not provided']
        self.assertItemsEqual(expectedErrors, model.errors)


    def test_missing_productid(self):
        invalid_json = json_example.copy()
        invalid_json.pop("productId")
        expectedErrors = ["Invalid JSON: missing productId"]

        self.tryMissingData(invalid_json, expectedErrors)

    def test_missing_user(self):
        invalid_json = json_example.copy()
        invalid_json.pop("userId")
        expectedErrors = ["Invalid JSON: missing userId"]
        self.tryMissingData(invalid_json, expectedErrors)

    def test_missing_score(self):
        invalid_json = json_example.copy()
        invalid_json.pop("score")
        expectedErrors = ["Invalid JSON: missing score"]
        self.tryMissingData(invalid_json, expectedErrors)

    def test_score_invalidTypeString(self):
        invalid_json = json_example.copy()
        invalid_json["score"] = "5.2"
        expectedErrors = ["Invalid JSON: field score has invalid type"]
        self.tryMissingData(invalid_json, expectedErrors)

    def test_missing_summary(self):
        invalid_json = json_example.copy()
        invalid_json.pop("summary")
        expectedErrors = ["Invalid JSON: missing summary"]
        self.tryMissingData(invalid_json, expectedErrors)

    def test_missing_text(self):
        invalid_json = json_example.copy()
        invalid_json.pop("text")
        expectedErrors = ["Invalid JSON: missing text"]
        self.tryMissingData(invalid_json, expectedErrors)

    def test_missing_profileName(self):
        invalid_json = json_example.copy()
        invalid_json.pop("profileName")
        expectedErrors = ["Invalid JSON: missing profileName"]
        self.tryMissingData(invalid_json, expectedErrors)


    def test_retrieve_last_20_reviews(self):
        reviewDAMock = MagicMock()

        mockValues = []
        for x in range(0, 20):
            mockValues.append(json_example)
        reviewDAMock.retrieveReviews.return_value = mockValues

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()

        model.productId = "1"
        model.retrieveReviews()

        self.assertEquals(20, len(model.reviews))
        reviewDAMock.retrieveReviews.assert_called_once_with("1")

    def test_retrieve_last_20_reviews_fromtoken(self):
        reviewDAMock = MagicMock()

        mockValues = []
        for x in range(0, 20):
            mockValues.append(json_example)
        reviewDAMock.retrieveReviews.return_value = mockValues

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()

        id = ObjectId()
        model.productId = "1"
        model.lastId = id 
        model.retrieveReviews()

        self.assertEquals(20, len(model.reviews))
        reviewDAMock.retrieveReviews.assert_called_once_with("1", id)

    def test_product_summary(self):
        reviewDAMock = MagicMock()

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()

        id = ObjectId()
        model.productId = "1"
        model.retrieveSummary()

        reviewDAMock.retrieveSummary.assert_called_once_with("1")

    def test_modifyReview(self):
        reviewDAMock = MagicMock()

        def config(binder):
            binder.bind(ReviewDA, reviewDAMock)

        inject.clear_and_configure(config)

        model = ReviewModel()
        model.data = json_example
        model.update()

        reviewDAMock.update.assert_called_once_with(json_example)

if __name__ == '__main__':
    unittest.main()
