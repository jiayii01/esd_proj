from invokes import invoke_http
from os import environ

bid_URL = environ.get('bidURL') or input("Enter Bidding service URL: ")  

# invoke book microservice to get all books
results = invoke_http(bid_URL, method='GET')

print( type(results) )
print()
print( results )

# invoke book microservice to create a bid
jobID = 3
freelancerID = "F3"
bid_details = {
    "biddingID":245629,
    "freelancerID":"F3",
    "jobID":3,
    "status":"Open",
    "dateTime":'2022-03-19 19:38:11',
    "price":'25.00'
}
create_results = invoke_http(
        bid_URL + "/add/" + str(jobID) +"/"+ str(freelancerID), method='POST', 
        json=bid_details
    )

print()
print( create_results )




