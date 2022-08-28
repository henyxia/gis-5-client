FROM python:3.10.6-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "/usr/local/bin/flask", "run", "--host=0.0.0.0" ]
