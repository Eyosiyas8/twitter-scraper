# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    jq \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Add Google's official repository and install the latest Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Run the scraper
CMD ["python", "Scraper/index_new.py"]