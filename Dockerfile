FROM python:3.8

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install chromium -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

#RUN pip install --upgrade pip


CMD ["python", "./__init__.py"]