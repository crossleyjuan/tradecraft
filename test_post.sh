for i in `seq 1 200`; do curl -H "Content-Type: application/json" -d '{ "userId": "1", "score": 5, "comments": "blah", "summary": "adsf", "text": "t5est", "profileName": "test" }' -X POST http://localhost:5000/reviews/1; done
