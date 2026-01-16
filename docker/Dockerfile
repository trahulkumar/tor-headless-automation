# Use a Python base image with X11 support
FROM python:3.10-slim

# Install system dependencies for Xvfb, VNC, and Tor Browser
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    wget \
    xz-utils \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libx11-xcb1 \
    libasound2 \
    libnss3 \
    python3-tk \
    python3-dev \
    scrot \
    ca-certificates \
    novnc \
    websockify \
    xterm \
    zenity \
    && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management
RUN wget -O- https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Create work directory
WORKDIR /app

# Download and install Tor Browser for Linux version 14.0.1 (Stable Archive)
RUN wget https://archive.torproject.org/tor-package-archive/torbrowser/14.0.1/tor-browser-linux-x86_64-14.0.1.tar.xz \
    && tar -xf tor-browser-linux-x86_64-14.0.1.tar.xz \
    && rm tor-browser-linux-x86_64-14.0.1.tar.xz \
    && mv tor-browser /app/tor-browser-bundle \
    && sed -i 's/`id -u`" -eq 0/`id -u`" -eq 1/g' /app/tor-browser-bundle/Browser/start-tor-browser

# Copy project files
COPY . .

# Install Python dependencies
RUN uv sync

# Create a shell script to start the environment
RUN echo '#!/bin/bash\n\
    rm -f /tmp/.X99-lock\n\
    touch /root/.Xauthority\n\
    Xvfb :99 -screen 0 1280x1024x24 &\n\
    sleep 2\n\
    export DISPLAY=:99\n\
    fluxbox &\n\
    sleep 2\n\
    x11vnc -display :99 -nopw -listen localhost -xkb -forever &\n\
    # Start noVNC bridge\n\
    websockify --web /usr/share/novnc/ 6080 localhost:5900 &\n\
    sleep 2\n\
    \n\
    if [ $# -gt 0 ]; then\n\
    echo "Running custom command: $@"\n\
    exec "$@"\n\
    else\n\
    echo "Running repeater automation (Docker)..."\n\
    exec uv run tor-repeat\n\
    fi\n\
    ' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Environment variables
ENV DISPLAY=:99
ENV XAUTHORITY=/root/.Xauthority
ENV TOR_BROWSER_DOCKER_PATH=/app/tor-browser-bundle/Browser/start-tor-browser

# Start the environment
ENTRYPOINT ["/app/entrypoint.sh"]
