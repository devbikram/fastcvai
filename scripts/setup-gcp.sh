#!/bin/bash

# GCP CI/CD Setup Script
# This script helps set up the Google Cloud Platform resources needed for CI/CD

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI is not installed. Please install it first:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project information
echo "Enter your GCP Project ID:"
read -r PROJECT_ID

echo "Enter your GitHub username:"
read -r GITHUB_USERNAME

echo "Enter your GitHub repository name:"
read -r GITHUB_REPO

# Set the project
print_status "Setting GCP project to $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

# Get project number
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
print_status "Project number: $PROJECT_NUMBER"

# Enable required APIs
print_status "Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable iam.googleapis.com

# Create Artifact Registry repository
print_status "Creating Artifact Registry repository..."
if ! gcloud artifacts repositories describe cv-analyzer --location=us-central1 &> /dev/null; then
    gcloud artifacts repositories create cv-analyzer \
        --repository-format=docker \
        --location=us-central1 \
        --description="CV Analyzer Docker repository"
    print_status "Artifact Registry repository created"
else
    print_warning "Artifact Registry repository already exists"
fi

# Create service account
print_status "Creating service account..."
if ! gcloud iam service-accounts describe "github-actions@$PROJECT_ID.iam.gserviceaccount.com" &> /dev/null; then
    gcloud iam service-accounts create github-actions \
        --description="Service account for GitHub Actions" \
        --display-name="GitHub Actions"
    print_status "Service account created"
else
    print_warning "Service account already exists"
fi

# Grant permissions to service account
print_status "Granting permissions to service account..."
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

# Create Workload Identity Pool
print_status "Creating Workload Identity Pool..."
if ! gcloud iam workload-identity-pools describe github-pool --location=global &> /dev/null; then
    gcloud iam workload-identity-pools create "github-pool" \
        --location="global" \
        --description="Workload Identity Pool for GitHub Actions"
    print_status "Workload Identity Pool created"
else
    print_warning "Workload Identity Pool already exists"
fi

# Create Workload Identity Provider
print_status "Creating Workload Identity Provider..."
if ! gcloud iam workload-identity-pools providers describe github-provider --workload-identity-pool=github-pool --location=global &> /dev/null; then
    gcloud iam workload-identity-pools providers create-oidc "github-provider" \
        --location="global" \
        --workload-identity-pool="github-pool" \
        --issuer-uri="https://token.actions.githubusercontent.com" \
        --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository"
    print_status "Workload Identity Provider created"
else
    print_warning "Workload Identity Provider already exists"
fi

# Allow GitHub Actions to impersonate the service account
print_status "Configuring Workload Identity Federation..."
gcloud iam service-accounts add-iam-policy-binding \
    "github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.workloadIdentityUser" \
    --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/$GITHUB_USERNAME/$GITHUB_REPO"

print_status "Setup completed! 🎉"
echo ""
echo "Next steps:"
echo "1. Add the following secrets to your GitHub repository:"
echo "   - GCP_PROJECT_ID: $PROJECT_ID"
echo "   - WIF_PROVIDER: projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider"
echo "   - WIF_SERVICE_ACCOUNT: github-actions@$PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo "2. Push your code to the main or develop branch to trigger deployment"
echo ""
echo "3. Monitor the deployment in GitHub Actions and Google Cloud Console"
