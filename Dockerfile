FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install chromium -y


COPY . .
WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "./__init__.py"]