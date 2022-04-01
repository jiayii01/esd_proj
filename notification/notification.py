from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from setuptools import Require
from twilio.rest import Client
from invokesNotification import MyRequestClass
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import json
import amqp_setup

app = Flask(__name__)
CORS(app)


number =  "+6597277518"

# Custom HTTP Class
my_request_client = MyRequestClass()


def successful_notification(jobID):
    #os.getenv()
    client = Client("AC075d686f2b7e890f6f730a89037f731b", "b7c4fb4d1389aa98ce6006bcda44bcaa",
                http_client=my_request_client)

    message = client.messages \
    .create(
        to=number,
        body="Congrats! You have been selected for job " + jobID+", please login to check your job details.",
        from_="+12347203241"
    )

    msg = "Accept job published to RabbitMQ Exchange."

    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="Activity_Log", 
    body=msg)
    print(message)
    print("\nAccept job published to RabbitMQ Exchange.\n")

def jobConfirmation_notification(jobID):

    #os.getenv()
    client = Client("AC075d686f2b7e890f6f730a89037f731b", "b7c4fb4d1389aa98ce6006bcda44bcaa",
                http_client=my_request_client)

    message = client.messages \
    .create(
        to=number,
        body="Congrats! Your job " + jobID+", role has been filled. Please login to view the freelancer details",
        from_="+12347203241"
    )


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

successful_notification("123")