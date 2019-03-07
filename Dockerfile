FROM python:3.6
RUN pip install requests
RUN pip install PyInquirer
COPY . /app
WORKDIR /app
CMD python generate_credentials.py