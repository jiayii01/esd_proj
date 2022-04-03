FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./bidding.py .
CMD [ "python", "./bidding.py" ]




# set dbURL=mysql+mysqlconnector://root@localhost:3306/bidding

# docker build -t hullojalapenos/bidding:1.0 ./
