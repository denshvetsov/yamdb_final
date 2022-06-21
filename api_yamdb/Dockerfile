FROM python:3.9
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN ls -ls
# WORKDIR /app/api_yamdb
# RUN ls -ls

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 
