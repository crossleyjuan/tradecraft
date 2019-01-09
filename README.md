Readme
------

Note: This is the version 3 of the tradecraft, if you want to see the version2 check the branches

You may be best using virtualenv for python (https://virtualenv.pypa.io/en/latest/)

Then do virtualenv .
Then source bin/activate

Install dependencies with

pip install -r requirements.txt

Run with

export FLASK_ENV=development
FLASK_APP=sequencesvc.py flask run


Test with

curl -X PUT http://localhost:5000/sequence/customers
