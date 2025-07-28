FROM python:3.12-slim

WORKDIR /app
RUN pip3 install flask

COPY redeploy.py .

CMD ["python3", "redeploy.py"]
