FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash git
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt