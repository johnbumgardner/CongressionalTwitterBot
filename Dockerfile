FROM python:3.7-alpine

COPY /auth.json /
COPY /congress.py /
COPY requirements.txt /tmp
COPY legislators-current.json /
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /
CMD ["python3", "congress.py"]
