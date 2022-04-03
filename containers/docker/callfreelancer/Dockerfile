FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./invokes.py ./test_invoke_http.py ./
CMD [ "python", "./test_invoke_http.py" ]



# set dbURL=mysql+mysqlconnector://root@localhost:3306/freelancers

# docker build -t hullojalapenos/freelancers:1.0 ./

# docker build -t hullojalapenos/callfreelancer:1.0 ./

# docker run --name freelancers --network my-net -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/freelancers hullojalapenos/freelancers:1.0


#docker run -it --network my-net --rm hullojalapenos/callfreelancer:1.0