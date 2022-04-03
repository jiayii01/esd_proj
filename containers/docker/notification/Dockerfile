FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt twilio
COPY ./notification.py ./invokesNotification.py ./
CMD [ "python3", "./notification.py"]



