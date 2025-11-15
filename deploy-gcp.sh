#!/bin/bash

# Google Cloud Run Deployment Script

echo "🚀 Deploying to Google Cloud Run"

# Variables (update these)
PROJECT_ID="your-gcp-project-id"
SERVICE_NAME="job-search-automation"
REGION="us-central1"

echo "🔧 Setting up GCP project..."
gcloud config set project $PROJECT_ID

echo "📦 Building container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --memory 512Mi \
  --timeout 3600 \
  --set-env-vars ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY,JOB_KEYWORDS="$JOB_KEYWORDS",JOB_LOCATION="$JOB_LOCATION" \
  --no-allow-unauthenticated

echo "✅ Deployment complete!"
echo "Service URL:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)'
