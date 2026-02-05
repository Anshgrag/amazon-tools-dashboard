#!/bin/bash

echo "Starting Docker..."
sudo systemctl start docker

echo "Starting media stack..."
docker compose up -d

echo "Opening services..."
xdg-open http://localhost:7878   # Radarr
xdg-open http://localhost:8989   # Sonarr
xdg-open http://localhost:8096   # Jellyfin
