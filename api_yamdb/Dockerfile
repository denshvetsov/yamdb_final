FROM python:3.7
WORKDIR /app
COPY . .
RUN pip3 install -r api_yamdb/equirements.txt --no-cache-dir
CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ] 
