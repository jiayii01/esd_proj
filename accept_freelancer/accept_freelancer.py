from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

#import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

job_URL = "http://localhost:5001/job"
bidding_URL = "http://localhost:5003/bidding"


@app.route("/accept_freelancer", methods=['POST'])   
def accept_freelancer():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            #1. Get the bidding id 123 for eg
            data = request.get_json()
            # print(data)
            bidInfo = chosenBidding(data['biddingID'])
            print(bidInfo)
            #2. Update the bidding status
            newStatus = updateBiddingStatus(data)
            print(newStatus)
            # # job = request.get_json()   #get the job data 
            print("\nAccept freelancer")
            # # # do the actual work
            # # # 3. Update job status to "filled"
            jobChosen = newStatus['data']["jobID"]
            freelancerChosen = newStatus['data']["freelancerID"]
            print(jobChosen, freelancerChosen)
            result =  updateJobStatus(jobChosen,freelancerChosen)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
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
      "status": "Filled"
    }
    job_result = invoke_http(job_URL+"/"+str(jobId), method='PUT', json=freelancerAndStatus)
    print('update_result:', job_result)
  
    # Check the job result; if a failure, send it to the error microservice.
    code = job_result["code"]
    message = json.dumps(job_result)

    if code not in range(200, 300):
        print("error")
    else: 
        print("successful")
        return job_result


def updateBiddingStatus(bidding):
    # Invoke the bidding microservice
    print('\n-----Invoking bidding microservice-----')
    biddingStatus = {
      "status": "Chosen"
    }
    bidding_result = invoke_http(bidding_URL+"/update/"+str(bidding["biddingID"]), method='PUT', json=biddingStatus)
    print('update_result:', bidding_result)
  
    # Check the order result; if a failure, send it to the error microservice.
    code = bidding_result["code"]
    message = json.dumps(bidding_result)

    if code not in range(200, 300):
        print("error")
    else: 
        print("successful")
        return bidding_result


def chosenBidding(id):   #retrieve bidding info that we chose by bidding ID
   # Invoke the bidding microservice
    print('\n-----Invoking bidding microservice-----')
    bidding_result = invoke_http(bidding_URL+"/biddingID/"+ str(id), method='GET')
    print('chosen result:', bidding_result)
  
    # Check the order result; if a failure, send it to the error microservice.
    code = bidding_result["code"]
    message = json.dumps(bidding_result)
    
    if code not in range(200, 300):
        print("error")
    else: 
        print("successful")
        return bidding_result
    

"""""

for amqp
    if code not in range(200, 300):
        # Inform the error microservice
        #print('\n\n-----Invoking error microservice as order fails-----')
        print('\n\n-----Publishing the (job error) message with routing_key=job.error-----')

        # invoke_http(error_URL, method="POST", json=order_result)
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
        # make message persistent within the matching queues until it is received by some receiver 
        # (the matching queues have to exist and be durable and bound to the exchange)

        # - reply from the invocation is not used;
        # continue even if this invocation fails        
        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), job_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"order_result": job_result},
            "message": "Order creation failure sent for error handling."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        # 4. Record new order
        # record the activity log anyway
        #print('\n\n-----Invoking activity_log microservice-----')
        print('\n\n-----Publishing the (order info) message with routing_key=order.info-----')        

        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="order.info", 
            body=message)
  
    print("\nOrder published to RabbitMQ Exchange.\n")
    # - reply from the invocation is not used;
    # continue even if this invocation fails
    
    # 5. Send new order to shipping
    # Invoke the shipping record microservice
    print('\n\n-----Invoking shipping_record microservice-----')    
"""""  
    


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
