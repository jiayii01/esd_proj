FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./freelancers.py .
CMD [ "python", "./freelancers.py" ]


# set dbURL=mysql+mysqlconnector://root@localhost:3306/freelancers


