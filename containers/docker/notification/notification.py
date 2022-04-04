from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from setuptools import Require
from twilio.rest import Client
from invokesNotification import MyRequestClass
import json

app = Flask(__name__)
CORS(app)


number =  "+6597277518"  #change this if you want the message to send to your phone

# Custom HTTP Class
my_request_client = MyRequestClass()

@app.route("/notification/<int:jobID>", methods=['GET'])
def successful_notification(jobID):
    #os.getenv()
    #freelancer side
    print("here")
    client = Client("AC075d686f2b7e890f6f730a89037f731b", "00cb3e1d17529296ec27ee6fcaa4ceab",
                http_client=my_request_client)

    message = client.messages \
    .create(
        to=number,
        body="Congrats! You have been selected for job " + str(jobID)+", please login to check your job details.",
        from_="+12347203241"
    )

    msg = "Accept job published to RabbitMQ Exchange."

    print(message)
    print("\nAccept job published to RabbitMQ Exchange.\n")


    #job poster side

    message2 = client.messages \
    .create(
        to=number,
        body="Congrats! Your job " + str(jobID)+", role has been filled. Please login to view the freelancer details",
        from_="+12347203241"
    )

    return "success"


@app.route("/broadcast_notification/<int:jobID>", methods=['GET'])
def broadcast_notification(jobID):
    #os.getenv()
    client = Client("AC075d686f2b7e890f6f730a89037f731b", "b7c4fb4d1389aa98ce6006bcda44bcaa",
                http_client=my_request_client)

    message = client.messages \
    .create(
        to=number,
        body=jobID+ " is available for application. Please login to sign up for this job",
        from_="+12347203241"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)