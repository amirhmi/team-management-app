

# syntax=docker/dockerfile:1.4

FROM python:3.8.5
WORKDIR /teamManagement
COPY requirements.txt /teamManagement
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /teamManagement
EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]