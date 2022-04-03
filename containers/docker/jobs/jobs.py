from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
import requests
# from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/jobs'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# CORS(app)

class Job(db.Model):
    __tablename__ = 'jobs'

    jobID = db.Column(db.Integer(6), primary_key=True,autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(10))
    deliveryDate = db.Column(db.Date, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    pickUpLocation = db.Column(db.String(1024), nullable=False)
    destination = db.Column(db.String(1024), nullable=False)
    freelancerID = db.Column(db.Integer(6))
    distance = db.Column(db.String(11), nullable=False)

    def __init__(self, name, price, description, status, deliveryDate, deadline, pickUpLocation, destination, freelancerID, distance):
        # self.jobID = jobID
        self.name = name
        self.price = price
        self.description = description
        self.status = status
        self.deliveryDate = deliveryDate
        self.deadline = deadline
        self.pickUpLocation = pickUpLocation
        self.destination = destination
        self.freelancerID = freelancerID
        self.distance = distance

    def json(self):
        return {"jobID": self.jobID, "name": self.name, "price": self.price, "description": self.description, "status": self.status, "deliveryDate": self.deliveryDate, "pickUpLocation": self.pickUpLocation, "destination": self.destination, "freelancerID": self.freelancerID, "distance": self.distance}

@app.route("/jobs")
def get_all():
    joblist = Job.query.all()
    if len(joblist):
        return jsonify(
            {
              "code": 200,
              "data": {
                  "jobs": [job.json() for job in joblist]
              }
            }
        )  
    return jsonify(
        {
          "code": 404,
          "message": "There are no jobs."
        }
    ), 404

@app.route("/jobs/<int:jobID>")
def find_by_jobID(jobID):
    job = Job.query.filter_by(jobID=jobID).first()
    if job:
        return jsonify(
            {
              "code": 200,
              "data": job.json()
            }
        )
    return jsonify(
        {
          "code": 404,
          "message": "Job doesn't exist."
        }
    ), 404


@app.route("/jobs", methods=['POST'])
def create_job(jobID):
    if (Job.query.filter_by(jobID=jobID).first()):
        return jsonify(
            {
              "code": 400,
              "data": {
                  "jobID": jobID
              },
              "message": "Job already exists."
            }
        ), 400

    data = request.get_json()
    
    url = "https://maps.googleapis.com/maps/api/directions/json?origin="+data["pickUpLocation"][:6]+",Singapore&destination="+data["destination"][:6]+",Singapore&key=AIzaSyCR5bhybFFnGTii7iY70BOShkkKnYTHj2E"
    payload={}
    headers = {}
    output = requests.request("GET", url, headers=headers, data=payload)
    finaloutput = output.json()
    if not finaloutput["routes"]:
        data["distance"] = "unavailable"
    else:
        data["distance"] = finaloutput["routes"][0]["legs"][0]["distance"]["text"]
        data["status"] = "NEW"
    job = Job(jobID, **data)

    try:
        db.session.add(job)
        db.session.commit()
    except:
        return jsonify(
            {
              "code": 500,
              "data": {
                  "jobID": jobID
              },
              "message": "An error occurred creating the job."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": job.json()
        }
    ), 201

@app.route("/jobs/<int:jobID>", methods=['PUT'])
def update_job(jobID):
    job = Job.query.filter_by(jobID=jobID).first()
    if job:
        data = request.get_json()
        for col in data:
          if col == "name":
            job.name = data['name']
          if col == "price":
            job.price = data['price']
          if col == "description":
            job.description = data['description']
          if col == "status":
            job.status = data['status']
          if col == "deliveryDate":
            job.deliveryDate = data['deliveryDate']
          if col == "deadline":
            job.deadline = data['deadline']
          if col == "destination":
            job.destination = data['destination']
          if col == "freelancerID":
            job.freelancerID = data['freelancerID']
          if col == "distance":
            job.distance = data['distance']

        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": job.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "jobID": jobID
            },
            "message": "Job not found."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001, debug=True)








