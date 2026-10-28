FROM python:3.12-slim

WORKDIR /app

# Copy Python Dependencies
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask application
COPY app.py ./

# Directory for persistent submission data
RUN mkdir -p /data

ENV PYTHONUNBUFFERED=1
ENV DATA_FILE=/data/submission.json

EXPOSE 5000

CMD [ "python" , "app.py" ]