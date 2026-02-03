#!/bin/bash
set -e

# ===== CONFIG =====
APP_NAME="app"
EC2_USER="ubuntu"
EC2_HOST="ec2-35-154-207-200.ap-south-1.compute.amazonaws.com"
PEM_KEY="/Users/maheswaranm/Downloads/makemystayrealty.pem"

REMOTE_DIR="/home/ubuntu/app"
VENV_DIR="$REMOTE_DIR/venv"

APP_MODULE="app.main:app"
PORT=8000

# ===== CLEANUP & PREPARE =====
echo "🧹 Cleaning up old deployment..."
ssh -i "$PEM_KEY" $EC2_USER@$EC2_HOST << EOF
mkdir -p $REMOTE_DIR
cd $REMOTE_DIR
rm -rf app dist build *.spec app.log
EOF

# ===== UPLOAD SOURCE =====
echo "📦 Uploading source files..."
scp -i "$PEM_KEY" -r \
  app \
  requirements.txt \
  .env.production \
  $EC2_USER@$EC2_HOST:$REMOTE_DIR/

# ===== SETUP & RUN ON EC2 =====
echo "🚀 Setting up & running FastAPI on EC2..."
ssh -i "$PEM_KEY" $EC2_USER@$EC2_HOST << EOF
set -e

cd $REMOTE_DIR

echo "🔧 Installing system packages..."
sudo apt update -y
sudo apt install -y python3 python3-venv python3-pip

echo "🐍 Creating venv (if missing)..."
if [ ! -d "$VENV_DIR" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "♻️ Stopping existing app..."
pkill -f "uvicorn $APP_MODULE" || true

echo "🌱 Loading production envs..."
set -a
source .env.production
set +a

echo "▶️ Starting FastAPI (background)..."
nohup uvicorn $APP_MODULE \
  --host 0.0.0.0 \
  --port $PORT \
  --workers 1 \
  > app.log 2>&1 &

deactivate
exit
EOF

echo "✅ Deploy complete. FastAPI is running."