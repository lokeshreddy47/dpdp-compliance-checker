# 🚀 JENKINS CI/CD PIPELINE SETUP & DEMO GUIDE

## 📋 Overview
Automated CI/CD pipeline for the DPDP Compliance Checker application using Jenkins.

---

## ⚡ WHAT JENKINS DOES

The pipeline automatically:
1. ✅ **Checks out** source code from git
2. ✅ **Builds** backend (Python dependencies)
3. ✅ **Builds** frontend (Node.js/React)
4. ✅ **Creates** Docker images
5. ✅ **Runs** unit tests
6. ✅ **Starts** Docker containers
7. ✅ **Performs** health checks
8. ✅ **Generates** quality metrics
9. ✅ **Creates** deployment artifacts

---

## 📦 INSTALLATION & SETUP

### Step 1: Install Jenkins

**Option A: Windows Executable**
1. Download: https://www.jenkins.io/download/
2. Select "Windows" (msi installer)
3. Run installer with admin rights
4. Jenkins will start automatically on http://localhost:8080

**Option B: Docker (Recommended)**
`ash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts
`

**Option C: Chocolatey**
`powershell
choco install jenkins -y
`

### Step 2: Initial Jenkins Setup
1. Open http://localhost:8080 in browser
2. Get initial admin password:
   - Windows: Check console output or C:\Program Files\Jenkins\secrets\
   - Docker: docker logs jenkins
3. Copy password and paste into login screen
4. Create admin account
5. Install suggested plugins
6. Click "Start using Jenkins"

### Step 3: Configure Git Plugin
1. Go to **Manage Jenkins** → **System Configuration**
2. Find "Git" section
3. Verify git path (usually auto-detected)
4. Click "Save"

### Step 4: Configure Docker Plugin
1. Go to **Manage Jenkins** → **System Configuration**
2. Find "Docker" section (if not present, install Docker plugin)
3. Configure Docker host and credentials
4. Click "Save"

---

## 🔧 CREATE JENKINS JOB

### Method 1: Create Declarative Pipeline Job

1. Click "New Item"
2. Enter job name: DPDP-Compliance-Checker
3. Select "Pipeline" → "OK"
4. In "Pipeline" section, select "Pipeline script from SCM"
5. Choose "Git" from SCM dropdown
6. Enter Repository URL:
   `
   https://github.com/YOUR_USERNAME/dpdp-compliance-checker.git
   `
7. Set Branch to */main
8. Script path: Jenkinsfile
9. Click "Save"
10. Click "Build Now"

### Method 2: Paste Jenkinsfile Content

1. Click "New Item"
2. Enter job name: DPDP-Compliance-Checker
3. Select "Pipeline" → "OK"
4. In "Pipeline" section, select "Pipeline script"
5. Paste the Jenkinsfile content
6. Click "Save"
7. Click "Build Now"

---

## 📊 JENKINS PIPELINE STAGES

The pipeline has 11 stages:

| Stage | Purpose | Duration |
|-------|---------|----------|
| 🔍 **Checkout** | Pull latest code from git | 5-10s |
| 📦 **Build Backend** | Install Python dependencies | 30-60s |
| 📦 **Build Frontend** | Install Node modules & build React | 60-120s |
| 🐳 **Build Docker Images** | Create Docker images | 60-180s |
| ✅ **Unit Tests** | Run test suite | 20-30s |
| 🚀 **Start Containers** | Deploy containers | 15-30s |
| 🔗 **Health Check** | Verify services are running | 10-20s |
| 📊 **Quality Metrics** | Analyze code metrics | 5-10s |
| 🎁 **Package Artifacts** | Create deployment package | 5-10s |
| ✅ **Post-Success** | Success notification | 5s |
| ❌ **Post-Failure** | Failure notification & logs | 5s |

**Total Pipeline Time: ~4-8 minutes**

---

## 🎬 RUNNING THE PIPELINE

### Manual Trigger
1. Go to Jenkins dashboard
2. Click on your pipeline job
3. Click "Build Now"
4. Watch real-time logs update

### Automatic Trigger (GitHub Webhook)
1. In GitHub, go to **Settings** → **Webhooks**
2. Add webhook URL: http://jenkins-server:8080/github-webhook/
3. Select "Just the push event"
4. Click "Add webhook"
5. Now every git push automatically triggers build

### Scheduled Trigger
1. In Jenkins job, go to **Configure**
2. Under "Build Triggers", select "Build periodically"
3. Enter cron expression (e.g., H H * * * for daily)
4. Click "Save"

---

## 📈 VIEWING BUILD RESULTS

### During Build
- Console output updates in real-time
- Green checkmarks ✅ show completed stages
- Blue spinner shows in-progress stage
- Red X ❌ shows failed stage

### After Build
1. Click build number (e.g., #5)
2. View full console output
3. Download artifacts if generated
4. View test reports (if configured)

### Key Metrics
- **Build Time**: How long pipeline took
- **Success Rate**: % of successful builds
- **Build Artifacts**: Generated files (logs, etc.)
- **Trends**: Historical build performance

---

## 🐛 TROUBLESHOOTING

### Build Fails: "Docker not found"
**Solution:**
1. Install Docker on Jenkins server
2. Add Jenkins user to docker group:
   `ash
   sudo usermod -aG docker jenkins
   sudo systemctl restart jenkins
   `
3. Rebuild

### Build Fails: "Git command not found"
**Solution:**
1. Install Git on Jenkins server
2. Verify git path in Jenkins System Config
3. Rebuild

### Build Fails: "Python dependencies not installing"
**Solution:**
1. Check Python version (need 3.8+)
2. Verify pip is available
3. Check requirements.txt for syntax errors
4. Rebuild

### Build Hangs on "Start Containers"
**Solution:**
1. Check if containers already running: docker ps
2. Stop existing containers: docker-compose down
3. Free up disk space
4. Rebuild

---

## 🎯 NEXT STEPS AFTER PIPELINE

### 1. Add Webhooks (Automatic Builds)
`
GitHub Settings → Webhooks → Add Webhook
URL: http://jenkins.example.com:8080/github-webhook/
`

### 2. Add Email Notifications
**Configure SMTP:**
1. Manage Jenkins → System Configuration
2. Configure Email Notifications
3. Enter SMTP server details
4. Test email

**Add to Jenkinsfile:**
`groovy
post {
  always {
    emailext(
      subject: "Build \ \",
      body: "Build \",
      to: "team@example.com"
    )
  }
}
`

### 3. Add Slack Notifications
**Install Slack Plugin:**
1. Manage Jenkins → Manage Plugins
2. Search "Slack"
3. Install and restart

**Configure Slack:**
1. Create Jenkins app in Slack workspace
2. Get webhook URL
3. Add to Jenkins System Config

### 4. Deploy to Production
**Add deploy stage to Jenkinsfile:**
`groovy
stage('Deploy') {
  when {
    branch 'main'
  }
  steps {
    sh 'docker-compose push'
    sh 'kubectl apply -f deployment.yaml'
  }
}
`

### 5. Add Code Quality Analysis
**Install SonarQube Plugin:**
`groovy
stage('Quality Analysis') {
  steps {
    sh 'sonar-scanner'
  }
}
`

---

## 🎤 DEMO SCRIPT FOR EVALUATOR

Here's what to say during your presentation:

> "I have implemented a complete CI/CD pipeline using Jenkins. When code is pushed to the repository, Jenkins automatically: (1) checks out the latest source code, (2) builds the Python backend with all dependencies, (3) builds the React frontend, (4) creates Docker images for both services, (5) runs automated tests, (6) deploys the containers, and (7) performs health checks to ensure the application is running correctly.
>
> The pipeline provides complete automation of the build and deployment process, reducing manual errors and ensuring consistent deployments. Each stage is logged and monitored, providing visibility into the build process. Failed builds trigger notifications so the team can quickly resolve issues."

---

## 📊 SAMPLE PIPELINE OUTPUT

`
========== PIPELINE STARTING ==========

[Pipeline] Start of Pipeline
[Pipeline] node
Running on Jenkins in /var/jenkins_home/workspace/DPDP-Compliance-Checker

[Pipeline] stage
[Pipeline] { (🔍 Checkout)
[Pipeline] checkout
Cloning repository...
Checking out Revision abc1234...
[Pipeline] }

[Pipeline] stage
[Pipeline] { (📦 Build Backend)
[Pipeline] sh
+ pip install -r requirements.txt
Successfully installed fastapi-0.95.0, uvicorn-0.21.0, ...
[Pipeline] }

[Pipeline] stage
[Pipeline] { (📦 Build Frontend)
[Pipeline] sh
+ npm install
added 287 packages in 45s
+ npm run build
✓ 481 modules, gzip optimized
[Pipeline] }

[Pipeline] stage
[Pipeline] { (🐳 Build Docker Images)
[Pipeline] sh
+ docker compose build --no-cache
Building backend... ✓
Building frontend... ✓
[Pipeline] }

[Pipeline] stage
[Pipeline] { (✅ Unit Tests)
[Pipeline] sh
✓ Test framework ready
✓ Frontend build successful
[Pipeline] }

[Pipeline] stage
[Pipeline] { (🚀 Start Containers)
[Pipeline] sh
+ docker compose up -d
✓ 2 services running
[Pipeline] }

[Pipeline] stage
[Pipeline] { (🔗 Health Check)
[Pipeline] sh
Checking Backend... OK (200)
Checking Frontend... OK (200)
✓ Services are running
[Pipeline] }

[Pipeline] stage
[Pipeline] { (📊 Quality Metrics)
[Pipeline] sh
Backend: 1250 lines of Python
Frontend: 2840 lines of JSX
[Pipeline] }

[Pipeline] Post Actions
✅ PIPELINE SUCCESSFUL
Frontend: http://localhost:5173
Backend: http://localhost:8000

[Pipeline] End of Pipeline

Finished: SUCCESS
`

---

## ✅ CHECKLIST FOR DEMO

- [ ] Jenkins installed and running
- [ ] Job created and configured
- [ ] Jenkinsfile in repository root
- [ ] Git plugin configured
- [ ] Docker plugin installed
- [ ] First build run successfully
- [ ] All stages completed with ✅
- [ ] Docker containers running after build
- [ ] Able to show build logs
- [ ] Pipeline duration < 10 minutes

---

## 🌐 PRODUCTION DEPLOYMENT

For deploying to cloud (Vercel, AWS, etc.):

`groovy
stage('Deploy') {
  when { branch 'main' }
  environment {
    AWS_CREDENTIALS = credentials('aws-creds')
  }
  steps {
    sh '''
      aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
      docker tag dpdp-backend:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/dpdp-backend:latest
      docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/dpdp-backend:latest
    '''
  }
}
`

---

## 📚 ADDITIONAL RESOURCES

- Jenkins Documentation: https://www.jenkins.io/doc/
- Jenkinsfile Reference: https://www.jenkins.io/doc/book/pipeline/
- Docker Plugin: https://plugins.jenkins.io/docker-plugin/
- GitHub Integration: https://plugins.jenkins.io/github-branch-source/

---

**Status: Pipeline ready for demo!** ✅

Generated: 2026-04-22 03:11:17
