Readme
------

Note: This is the version2 of the project, for latest version use the master

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
