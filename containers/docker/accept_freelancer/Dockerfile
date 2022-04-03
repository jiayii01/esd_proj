FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt twilio pika -r amqp.reqs.txt
COPY ./accept_freelancer.py ./invokes.py ./invokesNotification.py ./amqp_setup.py ./
CMD [ "python", "./accept_freelancer.py" ]
