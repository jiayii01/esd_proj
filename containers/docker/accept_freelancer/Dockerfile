FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt twilio pika
COPY ./accept_freelancer.py ./invokes.py ./amqp_setup.py ./invokesNotification.py ./
CMD [ "python", "./accept_freelancer.py" ]
