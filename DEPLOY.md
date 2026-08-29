# Manual AWS Deployment Guide

This guide walks you through manually deploying the Pathfinding Visualizer to AWS using the Free Tier. By completing this, you will have the Flask application running on an EC2 instance behind an Nginx reverse proxy, connected to a managed MySQL RDS instance.

## Prerequisites

1. **AWS Account**: Create a new AWS account if you don't have one (you get 12 months of Free Tier).
2. **Budget Alert**:
   - Go to **AWS Billing Dashboard** -> **Budgets**.
   - Create a new "Cost budget".
   - Set the threshold to $5. This ensures you'll get an email if you accidentally spin up resources outside the Free Tier.
3. **IAM User**:
   - Go to **IAM** (Identity and Access Management).
   - Create a new User (e.g., `deploy-admin`).
   - Grant it `AdministratorAccess` (for simplicity during learning).
   - Log out of your Root account and log back in using this new IAM User.

## Step 1: Launch the RDS Database (MySQL)

We launch the database first so it's ready when the application starts.

1. Go to **RDS** -> **Databases** -> **Create database**.
2. **Creation Method**: Standard create.
3. **Engine Options**: Select **MySQL**.
4. **Templates**: **Crucial**: Select **Free tier**.
5. **Settings**:
   - DB instance identifier: `pathfinder-db`
   - Master username: `app`
   - Master password: `<Choose a secure password>`
6. **Instance configuration**: Leave as `db.t3.micro` (or `db.t2.micro` depending on your region's free tier).
7. **Storage**: Leave defaults (20GB gp2). Uncheck "Enable storage autoscaling" to avoid surprise costs.
8. **Connectivity**:
   - **VPC**: Default VPC.
   - **Public access**: **No**. (The database should only be accessible by your EC2 instance, not the internet).
   - **VPC security group**: Create new. Name it `rds-sg`.
9. Click **Create database**. This takes a few minutes.

## Step 2: Launch the EC2 Instance

1. Go to **EC2** -> **Instances** -> **Launch instances**.
2. **Name**: `pathfinder-web`
3. **AMI (OS)**: Select **Ubuntu 22.04 LTS** (Free tier eligible).
4. **Instance type**: Select `t3.micro` or `t2.micro` (Free tier eligible).
5. **Key pair**: Click "Create new key pair". Name it `pathfinder-key`, select RSA and `.pem`. Download it and keep it safe.
6. **Network settings**:
   - Click **Edit**.
   - **VPC**: Select the Default VPC (same as RDS).
   - **Auto-assign Public IP**: Enable.
   - **Firewall (security groups)**: Create security group `web-sg`.
   - **Inbound Rules**:
     - Rule 1: SSH (Port 22) -> Source: **My IP** (Do NOT allow SSH from anywhere).
     - Rule 2: HTTP (Port 80) -> Source: **Anywhere (0.0.0.0/0)**.
     - Rule 3: HTTPS (Port 443) -> Source: **Anywhere (0.0.0.0/0)**.
7. Click **Launch instance**.

## Step 3: Allow EC2 to talk to RDS

1. Go to **EC2** -> **Security Groups**.
2. Select `rds-sg` (the one you created for the database).
3. Click **Edit inbound rules**.
4. Change the existing rule (or add a new one) for **MySQL/Aurora (Port 3306)**.
5. In the Source field, start typing `sg-` and select `web-sg` (the EC2 security group). 
6. Save rules. Now, *only* traffic coming from your EC2 instance is allowed into your database.

## Step 4: Deploy the Application

1. Get the **Public IPv4 address** of your EC2 instance from the EC2 console.
2. Get the **Endpoint** of your RDS database from the RDS console (e.g., `pathfinder-db.xxxxx.region.rds.amazonaws.com`).
3. SSH into your EC2 instance from your terminal:
   ```bash
   chmod 400 pathfinder-key.pem
   ssh -i pathfinder-key.pem ubuntu@<EC2_PUBLIC_IP>
   ```
4. Run the following commands on the server to install dependencies:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-venv nginx git
   ```
5. Clone the repository (replace with your actual repo URL):
   ```bash
   git clone <YOUR_REPO_URL> path-visualizer
   cd path-visualizer
   ```
6. Set up the Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
7. Set up the systemd service. We will use the `deploy/pathfinder.service` file:
   ```bash
   sudo cp deploy/pathfinder.service /etc/systemd/system/
   ```
   **Important:** Edit the file (`sudo nano /etc/systemd/system/pathfinder.service`) and update the `Environment` variables for `DB_HOST` (your RDS Endpoint) and `DB_PASSWORD`.
   
   Start the application:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start pathfinder
   sudo systemctl enable pathfinder
   ```
8. Set up Nginx as a reverse proxy:
   ```bash
   sudo cp deploy/nginx.conf /etc/nginx/sites-available/pathfinder
   sudo ln -s /etc/nginx/sites-available/pathfinder /etc/nginx/sites-enabled/
   sudo rm /etc/nginx/sites-enabled/default
   sudo systemctl restart nginx
   ```
9. Visit `http://<EC2_PUBLIC_IP>` in your browser. Your app should be live!

## Shut it down (Important!)

AWS charges for resources that are running. Even free tier has limits. When you are done demoing:

**To pause (Reversible, keeps data but stops EC2 billing):**
- Go to EC2 -> Select Instance -> **Instance state: Stop**. 
- *Note: RDS instances can only be stopped temporarily (for up to 7 days). They will turn back on automatically.*

**To destroy completely (Non-reversible, deletes everything, guarantees no bills):**
1. Go to RDS -> Select Database -> **Actions: Delete**. (Uncheck "Create final snapshot" to delete it faster).
2. Go to EC2 -> Select Instance -> **Instance state: Terminate**. 
3. (Optional) Delete the Elastic IPs and Security Groups if you want a clean slate.

---
*Note: This manual deployment process is great for understanding the components. Once you are comfortable with this, the natural next step is to automate these exact steps using Infrastructure-as-Code tools like Terraform.*
