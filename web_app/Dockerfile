FROM python:3.6

RUN apt-get update && \
    apt-get install build-essential

COPY ./ .

RUN pip install -r requirements.txt

WORKDIR /app

EXPOSE 8050

ENTRYPOINT ["python"]

CMD ["app.py"]