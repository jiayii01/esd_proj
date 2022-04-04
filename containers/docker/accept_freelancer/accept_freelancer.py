from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
from invokes import invoke_http
from invokesNotification import MyRequestClass
import amqp_setup
import pika
import json
import os, sys
from os import environ

app = Flask(__name__)
CORS(app)

job_URL = "http://jobs:5001/jobs" or environ.get('job_URL')
bidding_URL = "http://bidding:5002/bidding" or environ.get('bidding_URL')
notification_URL = "http://notification:5003/notification" or environ.get('shipping_record_URL')


@app.route("/accept_freelancer", methods=['POST'])   
def accept_freelancer():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            #1. Get the bidding info
            data = request.get_json()

            #2. Update the bidding status
            newStatus = updateBiddingStatus(data)
            print("\nAccept freelancer")
            print(newStatus)

            # # # do the actual work
            # # # 3. Update job status to "filled"
            jobChosen = newStatus['data']["jobID"]    #chosen jobID
            print(jobChosen)
            freelancerChosen = newStatus['data']["freelancerID"]   #chosen freelancerID
            print(jobChosen, freelancerChosen)
            result =  updateJobStatus(jobChosen,freelancerChosen)
            print('\n------------------------')
            print('\nresult: ', result)

            #4. Send notifications to the relevant stakeholder
            send_notification(newStatus['data']["jobID"])


            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "accept_freelancer.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def updateJobStatus(jobId,freelancerId):
    # Invoke the job microservice
    print('\n-----Invoking job microservice-----')

    freelancerAndStatus = {
      "freelancerID": freelancerId,
      "status": "FILLED"
    }

    job_result = invoke_http(job_URL+"/"+str(jobId), method='PUT', json=freelancerAndStatus)
    print('update_result:', job_result)
  
    # Check the job result; if a failure, send it to the error microservice.
    code = job_result["code"]
    message = json.dumps(job_result)

    amqp_setup.check_setup()

    #amqp handling
    if code not in range(200, 300):
        # Inform the error microservice

        print('\n\n-----Publishing the (job error) message with routing_key=job.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)


        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\njob status ({:d}) published to the RabbitMQ Exchange:".format(
            code), job_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": job_result,
            },
            "message": "job error sent for error handling."
        } 

    else: 
        # success job update 
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (job info) message with routing_key=job.info-----')        

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="job.info", 
            body=message)
    
        print("\njob published to RabbitMQ Exchange.\n")

        print("successful")
        return job_result


def updateBiddingStatus(bidding):
    # Invoke the bidding microservice
    print('\n-----Invoking bidding microservice-----')

    biddingStatus = {
      "status": "Chosen"
    }

    bidding_result = invoke_http(bidding_URL+"/update/"+str(bidding["biddingID"]), method='PUT', json=biddingStatus)
    print('update bid result:', bidding_result)
  
    # Check the bidding result; if a failure, send it to the error microservice.
    code = bidding_result["code"]
    message = json.dumps(bidding_result)

    amqp_setup.check_setup()

    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as update bidding status fails-----')
        print('\n\n-----Publishing the (bidding error) message with routing_key=bidding.error-----')

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nbidding status ({:d}) published to the RabbitMQ Exchange:".format(
            code), bidding_result)

        # 7. Return error
        return {
            "code": 400,
            "data": {
                "order_result": bidding_result,
            },
            "message": "job error sent for error handling."
        } 
    else: 
        # success job update 
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (bidding info) message with routing_key=bidding.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
#        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="bidding.info", 
#            body=message)
    
        print("\nbidding published to RabbitMQ Exchange.\n")

        print("successful")
        return bidding_result


def chosenBidding(id):   #retrieve bidding info that we chose by bidding ID
   # Invoke the bidding microservice
    print('\n-----Invoking choose bidding microservice-----')
    bidding_result = invoke_http(bidding_URL+"/biddingID/"+ str(id), method='GET')
    print('chosen bidding result:', bidding_result)
  
    # Check the order result; if a failure, send it to the error microservice.
    code = bidding_result["code"]
    message = json.dumps(bidding_result)
    
    if code not in range(200, 300):
        print("error")
    else: 
        print("successful")
        return bidding_result
    

def send_notification(jobID):
    print('\n-----Invoking notification microservice-----')
    invoke_http(notification_URL+"/"+str(jobID), method='GET')
    print("doneeee")


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for accepting a freelancer...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
