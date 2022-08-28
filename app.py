from flask import Flask
from flask.json import jsonify
from flask import request
import hashlib
import hmac

app = Flask(__name__)

@app.route("/version")
def version():
    return jsonify(version="0.0.2")

@app.post('/identify')
def identidy_post():

    req = request.get_json()
    if "challenge" not in req:
        pp = pprint.PrettyPrinter(indent=4, depth=6)
        debug_message = pp.pprint(req)
        return jsonify(error="invalid request"), 400

    team_id = "team_1"
    team_secret = hashlib.sha256(team_id.encode('utf-8')).hexdigest()
    digest = hmac.new(
        team_secret.encode('utf-8'),
        req['challenge'].encode('utf-8'),
        "sha256"
    ).hexdigest()

    return jsonify(digest=digest)
