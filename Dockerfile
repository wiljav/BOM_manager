# Dockerfile
FROM python:3-slim


WORKDIR /app


LABEL maintainer="William <will.jawad@gmail.com>"


ENV DUCKDB_PATH=/app/data/bom.duckdb
ENV STREAMLIT_SERVER_PORT=8501

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create data directory
RUN mkdir -p /app/data && mkdir -p /app/app && chmod +x start_streamlit.sh

# Expose port
EXPOSE $STREAMLIT_SERVER_PORT

# Run the app
CMD ["./start_streamlit.sh"]