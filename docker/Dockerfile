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
    autocutsel \
    && rm -rf /var/lib/apt/lists/*

# Install uv for dependency management globally
ENV UV_INSTALL_DIR="/usr/local/bin"
RUN wget -qO- https://astral.sh/uv/install.sh | sh

# Create a non-root user
RUN useradd -m -u 1000 toruser

# Create work directory
WORKDIR /app

# Download and install Tor Browser for Linux version 14.0.1 (Stable Archive)
# We do this as root, then change ownership
RUN wget https://archive.torproject.org/tor-package-archive/torbrowser/14.0.1/tor-browser-linux-x86_64-14.0.1.tar.xz \
    && tar -xf tor-browser-linux-x86_64-14.0.1.tar.xz \
    && rm tor-browser-linux-x86_64-14.0.1.tar.xz \
    && mv tor-browser /app/tor-browser-bundle \
    && chown -R toruser:toruser /app/tor-browser-bundle
# Removed the sed hack as we will run as non-root

# Create a convenience symlink so user can just type 'tor'
RUN ln -s /app/tor-browser-bundle/Browser/start-tor-browser /usr/local/bin/tor

# Copy project files and change ownership
COPY . .
RUN chown -R toruser:toruser /app

# Switch to non-root user
USER toruser

# Configure Fluxbox Menu (Right-Click Menu)
RUN mkdir -p /home/toruser/.fluxbox && \
    echo '[begin] (Tor Automation)' > /home/toruser/.fluxbox/menu && \
    echo '  [exec] (Start Tor Browser) {/usr/local/bin/tor}' >> /home/toruser/.fluxbox/menu && \
    echo '  [exec] (Terminal) {xterm}' >> /home/toruser/.fluxbox/menu && \
    echo '  [separator]' >> /home/toruser/.fluxbox/menu && \
    echo '  [reconfig] (Reconfigure)' >> /home/toruser/.fluxbox/menu && \
    echo '  [restart] (Restart)' >> /home/toruser/.fluxbox/menu && \
    echo '  [exit] (Exit)' >> /home/toruser/.fluxbox/menu && \
    echo '[end]' >> /home/toruser/.fluxbox/menu

# Install Python dependencies as the user
RUN uv sync

# Create a shell script to start the environment
# We write this as the user, so we have permission
RUN echo '#!/bin/bash\n\
    rm -f /tmp/.X99-lock\n\
    touch $HOME/.Xauthority\n\
    Xvfb :99 -screen 0 1280x1024x24 &\n\
    sleep 2\n\
    export DISPLAY=:99\n\
    fluxbox &\n\
    autocutsel -fork &\n\
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
ENV XAUTHORITY=/home/toruser/.Xauthority
ENV TOR_BROWSER_DOCKER_PATH=/app/tor-browser-bundle/Browser/start-tor-browser

# Start the environment
ENTRYPOINT ["/app/entrypoint.sh"]
