#!/bin/bash

# AWS EC2 Deployment Script
# This script helps deploy the job search automation to AWS EC2

echo "🚀 Deploying Job Search Automation to AWS EC2"

# Variables (update these)
EC2_HOST="your-ec2-instance.amazonaws.com"
EC2_USER="ec2-user"
KEY_FILE="path/to/your-key.pem"

echo "📦 Building Docker image..."
docker build -t job-search-automation .

echo "💾 Saving Docker image..."
docker save job-search-automation | gzip > job-search-automation.tar.gz

echo "📤 Uploading to EC2..."
scp -i $KEY_FILE job-search-automation.tar.gz $EC2_USER@$EC2_HOST:~/
scp -i $KEY_FILE docker-compose.yml $EC2_USER@$EC2_HOST:~/
scp -i $KEY_FILE .env $EC2_USER@$EC2_HOST:~/

echo "🔧 Setting up on EC2..."
ssh -i $KEY_FILE $EC2_USER@$EC2_HOST << 'EOF'
    # Load Docker image
    docker load < job-search-automation.tar.gz

    # Stop existing container
    docker-compose down

    # Start new container
    docker-compose up -d

    echo "✓ Deployment complete!"
    docker ps
EOF

echo "✅ Deployment finished!"
echo "Check status with: ssh -i $KEY_FILE $EC2_USER@$EC2_HOST 'docker logs job-search-automation'"
