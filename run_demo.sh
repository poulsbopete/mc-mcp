#!/bin/bash

# Mastercard API Demo Runner
# This script starts the demo application with full observability

set -e

echo "🚀 Starting Mastercard API Demo with OpenTelemetry"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Copying from env.example..."
    cp env.example .env
    echo "⚠️  Please edit .env with your credentials before running!"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

echo ""
echo "🔧 Configuration:"
echo "  Service: $SERVICE_NAME"
echo "  Version: $SERVICE_VERSION"
echo "  Environment: $ENVIRONMENT"
echo "  Port: $DEMO_PORT"
echo "  Mock Mode: $ENABLE_MOCK_MODE"
echo ""
echo "📊 OpenTelemetry Configuration:"
echo "  Endpoint: $ELASTIC_OTLP_ENDPOINT"
echo "  Service Name: $SERVICE_NAME"
echo ""
echo "🌐 Starting application..."
echo "  API Docs: http://localhost:$DEMO_PORT/docs"
echo "  Health: http://localhost:$DEMO_PORT/health"
echo ""

# Run the application
python demo_app.py

