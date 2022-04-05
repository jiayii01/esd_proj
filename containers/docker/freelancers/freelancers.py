from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
import requests
from flask_cors import CORS


# set dbURL=mysql+mysqlconnector://root@localhost:3306/freelancers
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS(app)
cors = CORS(app, resources={r"*": {"origins": "*"}})

class Freelancer(db.Model):
    __tablename__ = 'freelancers'

    freelancerID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __init__(self, name, phone):
        # self.freelancerID = freelancerID
        self.name = name
        self.phone = phone

    def json(self):
        return {"freelancerID": self.freelancerID,
         "name": self.name, 
         "phone": self.phone}

@app.route("/freelancers")
def get_all():
    freelancer_list = Freelancer.query.all()
    if len(freelancer_list):
        return jsonify(
            {
              "code": 200,
              "data": {
                  "freelancers": [freelancer.json() for freelancer in freelancer_list]
              }
            }
        )
    return jsonify(
        {
          "code": 404,
          "message": "There are no freelancers."
        }
    ), 404

@app.route("/freelancers/<int:freelancerID>")
def find_by_freelancerID(freelancerID):
    freelancer = Freelancer.query.filter_by(freelancerID=freelancerID).first()
    if freelancer:
        return jsonify(
            {
              "code": 200,
              "data": freelancer.json()
            }
        )
    return jsonify(
        {
          "code": 404,
          "message": "Freelancer doesn't exist."
        }
    ), 404


@app.route("/freelancers", methods=['POST'])
def create_freelancer():
    data = request.get_json()
    freelancer = Freelancer(**data)

    try:
        db.session.add(freelancer)
        db.session.commit()
    except:
        return jsonify(
            {
              "code": 500,
              "data": {
                  "freelancerID": freelancer
              },
              "message": "An error occurred creating the freelancer."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": freelancer.json()
        }
    ), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5004, debug=True)
