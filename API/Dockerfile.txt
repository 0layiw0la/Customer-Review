FROM python:3.9-slim

# Installing system dependencies required for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    fonts-liberation \
    libu2f-udev \
    xdg-utils \
    libgbm-dev \
    && apt-get clean

# Installing Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Installing ChromeDriver
RUN wget -q -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Seting environment variables for ChromeDriver
ENV PATH="/usr/local/bin:$PATH"

# Seting the working directory inside the container
WORKDIR /app

# Copying all project files into the container
COPY . .

# Installing Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Seting the default script to execute when the container starts
CMD ["python", "Main.py"]
