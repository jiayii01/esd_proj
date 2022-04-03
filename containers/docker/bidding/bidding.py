from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
from flask_cors import CORS
import json
# for windows people
# set dbURL=mysql+mysqlconnector://root@localhost:3306/bidding
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

CORS(app)

class Bidding(db.Model):
    __tablename__ = 'bidding'

    biddingID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # userID = db.Column(db.String(6), nullable=False)
    freelancerID = db.Column(db.Integer)
    jobID = db.Column(db.Integer)
    status = db.Column(db.String(10))
    dateTime = db.Column(db.DateTime, nullable=False, default=datetime.now)
    price = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, biddingID, freelancerID, jobID, status, dateTime, price):
        self.biddingID= biddingID
        # self.userID = userID
        self.freelancerID = freelancerID
        self.jobID = jobID
        self.status = status
        self.dateTime = dateTime
        self.price = price
        

    def json(self):
        return {"biddingID": self.biddingID,
        #  "userID": self.userID, 
         "freelancerID": self.freelancerID,
         "jobID": self.jobID,
          "status": self.status,
          "dateTime" : self.dateTime,
          "price" : self.price
          }

#get all bids
@app.route("/bidding")
def get_all():
    biddinglist = Bidding.query.all()
    if len(biddinglist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "bids": [bid.json() for bid in biddinglist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no bids."
        }
    ), 404


#getbids by status
@app.route("/bidding/status/<string:status>", methods=['GET'])
def find_bids_by_status(status):
    bids = Bidding.query.filter_by(status=status)
    if bids:
        return jsonify(
            {
                "code": 200,
                "data":{
                    "bids": [bid.json() for bid in bids]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No {{status}} bids found."
        }
    ), 404


#get bid by bidding ID
@app.route("/bidding/biddingID/<int:biddingID>", methods=['GET'])
def find_by_biddingID(biddingID):
    bid = Bidding.query.filter_by(biddingID=biddingID).first()
    if bid:
        return jsonify(
            {
                "code": 200,
                "data": bid.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bid not found."
        }
    ), 404

#get bids by job ID
@app.route("/bidding/jobID/<int:jobID>", methods=['GET'])
def find_by_jobID(jobID):
    bids = Bidding.query.filter_by(jobID=jobID).all()
    if bids:
        return jsonify(
            {
                "code": 200,
                "bids": [bid.json() for bid in bids]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Bids for job ID not found."
        }
    ), 404

#adding bids
@app.route("/bidding/add/<int:jobID>/<int:freelancerID>", methods=['POST'])
def create_bids(jobID,freelancerID):
    data = request.get_json()
    data["jobID"] = jobID
    data["freelancerID"] = freelancerID
    bid = Bidding(**data)
    check_bid_exist = Bidding.query.filter_by(jobID=jobID).filter_by(freelancerID=freelancerID).first()
    print(check_bid_exist)
    if (check_bid_exist):
        #if bid exists, delete old bid first then add new bid
        db.session.delete(check_bid_exist)
        db.session.commit()
        db.session.add(bid)
        db.session.commit()
        return jsonify(
            {
                "code": 204,
                "message": "Bid has been replaced."
            }
        ), 204

    try:
        db.session.add(bid)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the bid."
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": bid.json(),
            "message": "Bid has successfully been created"
        },
    ), 201

#update bid
@app.route("/bidding/update/<int:biddingID>", methods=['PUT'])
def update_bid(biddingID):
    bid = Bidding.query.filter_by(biddingID=biddingID).first()
    if bid:
        data = request.get_json()
        for item in data:
            if item == 'biddingID':
                bid.biddingID = data['biddingID']
            # if item =='userID':
            #     bid.userID = data['userID']
            if item =='freelancerID':
                bid.freelancerID = data['freelancerID']
            if item =='jobID':
                bid.jobID = data['jobID']
            if item =='status':
                bid.status = data['status']
            if item =='dateTime':
                bid.dateTime = data['dateTime']
            if item =='price':
                bid.price = data['price']
        
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": bid.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "biddingID": biddingID
            },
            "message": "Bid not found."
        }
    ), 404

#delete bid
@app.route("/bidding/delete/<int:biddingID>", methods=['DELETE'])
def delete_bid(biddingID):
    bid = Bidding.query.filter_by(biddingID=biddingID).first()
    if bid:
        db.session.delete(bid)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "biddingID":biddingID
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "biddingID": biddingID
            },
            "message": "Bid not found."
        }
    ), 404

#getting freelancer ID for the top 3 bids
@app.route("/bidding/<int:jobID>/filter", methods=['GET'])
def get_freelancer(jobID):
    bids = Bidding.query.filter_by(jobID=jobID).order_by(Bidding.price)
    
    
    if bids:
        for bid in bids:
            bid.json()
        
        return jsonify(
            {
                "code": 200,
                "bids": [bid.json() for bid in bids[0:3]]
            }
        )
        return jsonify(
            {
                "code": 404,
                "message": "No freelancers bidded for this job."
            }
        ), 404
            
        
# rendering templates
@app.route("/joblist")
def joblist():
    return render_template("bidjob.html")

@app.route("/jobdetails/<int:jobID>")
def jobdetails(jobID):
    return render_template("jobdetails.html", jobID=jobID)
# end

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)






