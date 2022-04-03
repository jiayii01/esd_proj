from invokes import invoke_http
from os import environ

freelancer_URL = environ.get('freelancerURL') or input("Enter Freelancer service URL: ")  

# invoke book microservice to get all books
results = invoke_http(freelancer_URL, method='GET')

print( type(results) )
print()
print( results )

# invoke freelancer microservice to create a freelancer
freelancerID = "F3"
freelancer_details = {
    "freelancerID":"F3",
    "name": "Georgia Hwang",
    "phone": 90304601
}
create_results = invoke_http(
        freelancer_URL + "/"  + freelancerID , method='POST', 
        json=freelancer_details
    )

print()
print( create_results )




