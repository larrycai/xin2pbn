FROM python:alpine

# docker run -it -p 8080:5000 -v $PWD:/app  -w /app larrycai/pbn

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

#CMD ["python","app.py"]
