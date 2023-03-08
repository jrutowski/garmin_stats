# app/Dockerfile

FROM python:3.9-slim

LABEL maintainer "Josh Rutowski  <rutowskijosh@gmail.com>"
# If you have any comment : LinkedIn - https://www.linkedin.com/in/josh-rutowski/

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/jrutowski/garmin_stats.git .
RUN pip3 install -r requirements.txt
RUN echo "Requirements installed"
WORKDIR /app/app

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]