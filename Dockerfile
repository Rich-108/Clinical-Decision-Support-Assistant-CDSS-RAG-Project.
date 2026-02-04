FROM python:3.11

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Give execution permission to the start script
RUN chmod +x start.sh

# Start the application
CMD ["./start.sh"]