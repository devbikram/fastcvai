# CV Analyzer - Full Stack Application with CI/CD Pipeline

This repository contains a complete CV Analyzer application with both frontend (Next.js) and backend (Python FastAPI) services, along with a CI/CD pipeline that automatically deploys to Google Cloud Platform.

## 🏗️ Architecture

- **Frontend**: Next.js with React, TypeScript, and Tailwind CSS
- **Backend**: Python FastAPI with file processing and AI-powered CV analysis
- **Deployment**: Single Docker container running both services with nginx proxy
- **CI/CD**: GitHub Actions with automated testing and deployment to GCP

## 📁 Project Structure

```
├── frontend/                 # Next.js frontend application
│   ├── src/app/             # Next.js app router
│   ├── package.json         # Frontend dependencies
│   └── next.config.js       # Next.js configuration
├── backend/                 # Python FastAPI backend
│   ├── app/                 # FastAPI application
│   │   ├── main.py         # Main FastAPI server
│   │   ├── utils.py        # Utility functions
│   │   └── ...             # Other modules
│   ├── requirements.txt    # Python dependencies
│   └── .env.local.example  # Environment variables template
├── .github/workflows/      # GitHub Actions workflows
├── Dockerfile             # Production multi-service container
├── nginx.conf            # Nginx reverse proxy configuration
├── docker-compose.yml    # Local development setup
└── scripts/             # Setup and utility scripts
```

## 🚀 Features

### Frontend Features
- **File Upload**: Support for PDF, DOCX, JPG, and PNG files
- **CV Analysis**: Real-time analysis with job matching
- **Interactive UI**: Modern, responsive design with Tailwind CSS
- **Progress Tracking**: Visual feedback for all operations
- **Error Handling**: Comprehensive error messages and validation

### Backend Features  
- **File Processing**: Handle PDF, DOCX, and image files with OCR
- **AI-Powered Analysis**: Advanced CV analysis using OpenAI
- **Database Integration**: SQLite database for session management
- **Text Extraction**: Support for multiple file formats
- **Health Monitoring**: Built-in health check endpoints
- **Security**: CORS, file validation, and secure file handling

### DevOps Features
- **Multi-stage Docker builds** for optimized production images
- **Nginx reverse proxy** for routing and load balancing
- **Automated testing** for both frontend and backend
- **Multi-environment deployment** (staging and production)
- **Security-first approach** with Workload Identity Federation

## � Local Development

### Prerequisites
- Node.js 18+ 
- Python 3.11+
- Docker and Docker Compose
- Git

### Quick Start

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd cv-analyzer
```

2. **Set up environment variables**:
```bash
# Frontend
cp frontend/.env.local.example frontend/.env.local

# Backend  
cp backend/.env.local.example backend/.env.local
```

3. **Run with Docker Compose**:
```bash
docker-compose up --build
```

4. **Access the application**:
- **Full Application**: http://localhost:8080 (nginx proxy)
- **Frontend Only**: http://localhost:3000 (Next.js dev server)
- **Backend API**: http://localhost:4000 (FastAPI server)

### Manual Development Setup

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

### Testing

**Run all tests**:
```bash
# Frontend tests
cd frontend && npm test

# Backend tests  
cd backend && python -m pytest
```

**Linting**:
```bash
# Frontend
cd frontend && npm run lint

# Backend
cd backend && python -m flake8 .
```

## 📊 API Endpoints

### Backend API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/analyze-cv` | Upload and analyze CV |

### Example API Usage

**Health Check**:
```bash
curl http://localhost:4000/
```

**Upload CV for Analysis**:
```bash
curl -X POST http://localhost:4000/api/analyze-cv \
  -F "file=@your-cv.pdf" \
  -F "current_job_title=Software Engineer" \
  -F "target_job_title=Senior Software Engineer" \
  -F "job_description=We are looking for a skilled developer..."
```

## 🐳 Docker Deployment

### Production Build
```bash
# Build the production image
docker build -t cv-analyzer .

# Run the container
docker run -p 8080:8080 cv-analyzer
```

### Environment Variables

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8080/api
NEXT_PUBLIC_APP_ENV=development
```

**Backend** (`.env.local`):
```bash
PYTHONPATH=/app/backend
PORT=4000
# Add your OpenAI API key and other environment variables
OPENAI_API_KEY=your_openai_api_key
```

## �📋 Prerequisites

1. **Google Cloud Project**: Create a GCP project
2. **GitHub Repository**: Your code repository
3. **Required GCP APIs**: Enable the following APIs in your GCP project:
   - Cloud Run API
   - Cloud Build API
   - Artifact Registry API (or Container Registry API)
   - IAM API

## 🔧 Setup Instructions

### 1. Configure Google Cloud Platform

#### Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable iam.googleapis.com
```

#### Create Artifact Registry Repository
```bash
gcloud artifacts repositories create cv-analyzer \
  --repository-format=docker \
  --location=us-central1 \
  --description="CV Analyzer Docker repository"
```

#### Create Service Account
```bash
# Create service account
gcloud iam service-accounts create github-actions \
  --description="Service account for GitHub Actions" \
  --display-name="GitHub Actions"

# Grant necessary permissions
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"
```

### 2. Setup Workload Identity Federation

#### Create Workload Identity Pool
```bash
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --description="Workload Identity Pool for GitHub Actions"
```

#### Create Workload Identity Provider
```bash
gcloud iam workload-identity-pools providers create-oidc "github-provider" \
  --location="global" \
  --workload-identity-pool="github-pool" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository"
```

#### Allow GitHub Actions to impersonate the service account
```bash
gcloud iam service-accounts add-iam-policy-binding \
  "github-actions@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/attribute.repository/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"
```

### 3. Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions):

| Secret Name | Description | Example Value |
|-------------|-------------|---------------|
| `GCP_PROJECT_ID` | Your GCP Project ID | `my-project-123456` |
| `WIF_PROVIDER` | Workload Identity Provider | `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider` |
| `WIF_SERVICE_ACCOUNT` | Service Account Email | `github-actions@PROJECT_ID.iam.gserviceaccount.com` |

### 4. Package.json Scripts

Ensure your `package.json` includes these scripts:
```json
{
  "scripts": {
    "build": "next build",
    "start": "next start",
    "test": "jest",
    "lint": "next lint"
  }
}
```

## 🔄 Deployment Workflow

### Automatic Deployment Triggers

- **Production**: Push to `main` branch → Deploy to production Cloud Run service
- **Staging**: Push to `develop` branch → Deploy to staging Cloud Run service
- **Testing**: Pull requests to `main` → Run tests only (no deployment)

### Manual Deployment

You can also trigger deployments manually using Cloud Build:
```bash
gcloud builds submit --config cloudbuild.yaml
```

## 🛠 Deployment Options

### Option 1: Cloud Run (Recommended)
- Fully managed serverless platform
- Automatic scaling to zero
- Pay per request
- Supports containers

### Option 2: App Engine
- Fully managed platform
- Automatic scaling
- Built-in security features
- Use `app.yaml` configuration

### Option 3: Cloud Build
- Custom build and deployment pipeline
- More control over the build process
- Use `cloudbuild.yaml` configuration

## 🔍 Monitoring and Debugging

### View Deployment Status
- Check GitHub Actions tab in your repository
- View logs in Google Cloud Console → Cloud Build
- Monitor application in Google Cloud Console → Cloud Run

### Common Issues and Solutions

1. **Authentication Errors**
   - Verify Workload Identity Federation setup
   - Check service account permissions
   - Ensure GitHub secrets are correctly set

2. **Build Failures**
   - Check build logs in GitHub Actions
   - Verify Dockerfile syntax
   - Ensure all dependencies are listed in package.json

3. **Deployment Failures**
   - Check Cloud Run logs
   - Verify environment variables
   - Ensure health check endpoints are working

### Health Check Endpoint

Add a health check endpoint to your application:
```typescript
// pages/api/health.ts or app/api/health/route.ts
export async function GET() {
  return Response.json({ status: 'OK', timestamp: new Date().toISOString() });
}
```

## 🔐 Security Best Practices

1. **Use Workload Identity Federation** instead of service account keys
2. **Limit service account permissions** to minimum required
3. **Enable security headers** in your application
4. **Use HTTPS only** for production deployments
5. **Regularly update dependencies** and base images

## 📝 Environment Variables

Configure environment variables in your deployment:

### For Cloud Run:
- Set in GitHub Actions workflow under `env_vars`
- Or use Google Secret Manager for sensitive data

### For App Engine:
- Set in `app.yaml` under `env_variables`

## 🚨 Emergency Procedures

### Rollback Deployment
```bash
# Get previous revision
gcloud run revisions list --service=cv-analyzer-app --region=us-central1

# Rollback to previous revision
gcloud run services update-traffic cv-analyzer-app \
  --to-revisions=REVISION_NAME=100 \
  --region=us-central1
```

### Stop All Traffic
```bash
gcloud run services update-traffic cv-analyzer-app \
  --to-revisions=REVISION_NAME=0 \
  --region=us-central1
```

## 📞 Support

For issues with this CI/CD pipeline:
1. Check GitHub Actions logs
2. Review Google Cloud Build logs
3. Verify GCP service configurations
4. Check this documentation for troubleshooting steps

## 🔄 Updating the Pipeline

To modify the deployment pipeline:
1. Update `.github/workflows/deploy-to-gcp.yml`
2. Modify `Dockerfile` for container changes
3. Update `cloudbuild.yaml` for Cloud Build changes
4. Adjust `app.yaml` for App Engine configurations

Remember to test changes in a development environment before applying to production!
