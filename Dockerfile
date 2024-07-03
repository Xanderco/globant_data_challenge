FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# Ensure the data files are available for testing
RUN mkdir -p /mnt/data && cp -r data_challenge_files/* /mnt/data/

ENV FLASK_ENV=development

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]