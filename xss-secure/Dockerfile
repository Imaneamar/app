FROM python:3.9
WORKDIR /app
COPY app.py .
COPY templates ./templates
COPY static ./static
RUN pip install flask
CMD ["python", "app.py"]
