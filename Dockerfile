FROM python:3.5
RUN mkdir gdownload
WORKDIR gdownload
COPY . . 
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "gdownload"]
