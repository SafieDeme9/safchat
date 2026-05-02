#!/bin/bash
echo "🧹 Cleaning Docker..."

sudo docker-compose down -v --remove-orphans 2>/dev/null
sudo docker stop $(sudo docker ps -aq) 2>/dev/null || true
sudo docker rm $(sudo docker ps -aq) 2>/dev/null || true
sudo docker rmi $(sudo docker images -q) 2>/dev/null || true
sudo docker system prune -a -f 2>/dev/null || true
sudo docker volume prune -f 2>/dev/null || true

echo "✅ Clean complete"