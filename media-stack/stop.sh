#!/bin/bash

echo "Stopping media stack..."
docker compose down

echo "Stopping Docker..."
sudo systemctl stop docker

echo "All services stopped. Laptop is cool ❄️"
