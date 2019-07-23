FROM nikolaik/python-nodejs:python3.7-nodejs12
RUN pip install -r backend/requirements.txt
RUN cd frontend && npm install && cd ..
WORKDIR /backend
CMD python server.py > status.log 2>&1
EXPOSE 80