FROM python:3.11

LABEL authors="rurz"

RUN mkdir /app

COPY . /app

WORKDIR /app

EXPOSE 8501

RUN pip3 install -r requirements.txt

CMD ["streamlit", "run", "main.py", "--server.port", "8501"]
