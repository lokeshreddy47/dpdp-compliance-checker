FROM python:3.10

WORKDIR /app

# Install Python dependencies
COPY dpdp-backend/requirements.txt .
RUN pip install -r requirements.txt

COPY dpdp-backend/. .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

