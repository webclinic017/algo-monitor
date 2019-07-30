FROM nikolaik/python-nodejs:python3.7-nodejs12
COPY backend/ /app/backend
COPY frontend/ /app/frontend
WORKDIR /app
RUN pip install gunicorn
RUN pip install -r backend/requirements.txt
RUN cd frontend && npm install && npm run build && cd ..
CMD cd backend && gunicorn app:server -b localhost:80 > status.log 2>&1
EXPOSE 80