#!/bin/bash

# Eye Disease Detection - Quick Setup Script
echo "🏥 Setting up Eye Disease Detection Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p ml/models/weights
mkdir -p ml/data/processed
mkdir -p uploads
mkdir -p docker/grafana/{dashboards,datasources}
mkdir -p docker/ssl

# Copy environment files
echo "⚙️ Setting up environment..."
cat > backend/.env << EOF
DATABASE_URL=postgresql://postgres:postgres123@postgres:5432/eyedisease
REDIS_URL=redis://redis:6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
SECRET_KEY=your-production-secret-key-change-this-in-production
DEBUG=false
MODEL_PATH=ml/models/weights/best_model.pth
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
EOF

cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
EOF

# Create Grafana datasource config
cat > docker/grafana/datasources/prometheus.yml << EOF
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
EOF

# Create Nginx config
cat > docker/nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:8000;
    }
    
    upstream frontend {
        server frontend:3000;
    }
    
    server {
        listen 80;
        server_name localhost;
        
        # Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # Backend API
        location /api/ {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
        
        # API Documentation
        location /docs {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF

# Create Prometheus config
cat > docker/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
EOF

echo "🐳 Building and starting containers..."
cd docker
docker compose down 2>/dev/null
docker compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service health..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running"
else
    echo "❌ Backend failed to start"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend failed to start"
fi

if curl -s http://localhost:9090 > /dev/null; then
    echo "✅ Prometheus is running"
else
    echo "❌ Prometheus failed to start"
fi

echo ""
echo "🎉 Setup complete! Access the application:"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo "📊 Monitoring: http://localhost:3001 (Grafana - admin/admin123)"
echo "🔍 Metrics: http://localhost:9090 (Prometheus)"
echo ""
echo "⚠️  Note: You'll need to add a trained model to ml/models/weights/best_model.pth"
echo "   For testing without a model, the API will return mock responses."