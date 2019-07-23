FROM nikolaik/python-nodejs:python3.7-nodejs12
RUN cd backend && pip install -r requirements.txt && cd ..
RUN cd frontend && npm install && cd ..
WORKDIR /backend
CMD python server.py > status.log 2>&1
EXPOSE 80
