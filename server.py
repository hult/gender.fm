from flask import Flask, Blueprint, jsonify, request

import genderfm

app = Flask(__name__)
gfm = Blueprint('genderfm', __name__, static_folder='.', static_url_path='')

@gfm.route("/")
def index():
    return gfm.send_static_file("index.html")

@gfm.route("/genders")
def genders():
    return jsonify(genderfm.genderfm(request.args.get("access_token")))

app.register_blueprint(gfm)

if __name__ == "__main__":
    app.run(debug=True)
