from invokes import invoke_http
from os import environ

job_URL = environ.get('jobURL') or input("Enter Job service URL: ")  

# invoke book microservice to get all books
results = invoke_http(job_URL, method='GET')

print( type(results) )
print()
print( results )

# invoke book microservice to create a book
jobID = 5
job_details = {
    "deadline": "2022-04-13",
    "deliveryDate": "2022-04-15",
    "description": "Please deliver these cakes!",
    "destination": "765621 Marina Bay Sands 4",
    "name": "Cake Delivery",
    "pickUpLocation": "512456 Ubi Street 12 Blk 456 #11-28",
    "price": 21.0,
    "status": "NEW",
    "freelancerID": None
}
create_results = invoke_http(
        job_URL + "/" + str(jobID), method='POST', 
        json=job_details
    )

print()
print( create_results )
