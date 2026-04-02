FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY req.txt .
RUN pip install --upgrade pip
RUN pip install -r req.txt

# Copy project
COPY . .

# Run the application
CMD ["gunicorn", "H_M_S.wsgi:application", "--bind", "0.0.0.0:8000"]