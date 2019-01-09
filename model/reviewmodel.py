from da import ReviewDA
import inject

class ReviewModel():
    da = inject.attr(ReviewDA)
    data = None
    errors = None
    lastId = None

    def __init__(self):
        self.data = None
        self.errors = []
        self.lastId = None

    def _check(self, field, validTypes=[str, unicode]):
        if field not in self.data:
            self.errors.append("Invalid JSON: missing %s" % field)
        else:
            isValid = False
            dataType = type(self.data[field])
            for validType in validTypes:
                if dataType == validType:
                    isValid = True

            if not isValid:
                self.errors.append("Invalid JSON: field %s has invalid type" % field)

    def _validateData(self):
        if self.data is None:
            self.errors.append("json not provided")

        else:
            self._check("productId")
            self._check("userId")
            self._check("score", [int, float])
            self._check("summary")
            self._check("text")
            self._check("profileName")

    def save(self):
        self._validateData()
        if len(self.errors) == 0:
            reviewData = {
                    "userId": self.data["userId"],
                    "profileName": self.data["profileName"],
                    "score": self.data["score"],
                    "summary": self.data["summary"],
                    "text": self.data["text"]
                    }
            self.da.save(self.data["productId"], reviewData)

    def retrieveReviews(self):
        if self.lastId is not None:
            self.reviews = self.da.retrieveReviews(self.productId, self.lastId)
        else:
            self.reviews = self.da.retrieveReviews(self.productId)

    def retrieveSummary(self):
        self.summary = self.da.retrieveSummary(self.productId)

    def update(self):
        self.da.update(self.data)


