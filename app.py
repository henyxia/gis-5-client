from flask import Flask
from flask.json import jsonify
from flask import request
import hashlib
import hmac

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier

app = Flask(__name__)
version_name = "0.0.15"

# generics
def algo_class_generic_score(classifier_name):
    req = request.get_json()

    classifier = classifier_name(random_state=1)
    classifier.fit(
        req["X"],
        req["Y"],
    )
    correct_class = classifier.predict(req["test_value"])
    score = classifier.score(req["X"], req["Y"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        score=float(score),
    )

def algo_class_generic_precision(classifier_name):
    req = request.get_json()

    classifier = classifier_name(random_state=1)
    classifier.fit(
        req["X"],
        req["Y"],
    )
    correct_class = classifier.predict(req["test_value"])
    precisions = classifier.predict_proba(req["test_value"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        precision=float(precisions[0][correct_class[0]]),
    )

# routes
@app.route("/version")
def version():
    return jsonify(version=version_name)

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

@app.post('/algo/knn/class')
def algo_knn_class():
    req = request.get_json()

    neigh = KNeighborsClassifier(n_neighbors=5)
    neigh.fit(
        req["X"],
        req["Y"],
    )
    correct_class = neigh.predict(req["test_value"])
    precisions = neigh.predict_proba(req["test_value"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        precision=float(precisions[0][correct_class[0]]),
    )

@app.post('/algo/linear/class')
def algo_linear_class():
    req = request.get_json()

    classifier = RidgeClassifier()
    classifier.fit(
        req["X"],
        req["Y"],
    )
    correct_class = classifier.predict(req["test_value"])
    precision = classifier.score(req["X"], req["Y"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        precision=float(precision),
    )

@app.post('/algo/decision-tree/class')
def algo_decision_tree_class():
    req = request.get_json()

    classifier = DecisionTreeClassifier()
    classifier.fit(
        req["X"],
        req["Y"],
    )
    correct_class = classifier.predict(req["test_value"])
    precisions = classifier.predict_proba(req["test_value"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        precision=float(precisions[0][correct_class[0]]),
    )

@app.post('/algo/random-forest/class')
def algo_random_forest_class():
    req = request.get_json()

    classifier = RandomForestClassifier(random_state=1)
    classifier.fit(
        req["X"],
        req["Y"],
    )
    correct_class = classifier.predict(req["test_value"])
    precisions = classifier.predict_proba(req["test_value"])

    return jsonify(
        predicted_class=int(correct_class[0]),
        precision=float(precisions[0][correct_class[0]]),
    )

@app.post('/algo/svm/class')
def algo_linear_svc():
    return algo_class_generic_score(LinearSVC)

@app.post('/algo/mlp/class')
def algo_mlp_class():
    return algo_class_generic_precision(MLPClassifier)
