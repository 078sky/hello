# Deploying to DigitalOcean

This guide walks through deploying the Memory Agent application on DigitalOcean.

## Prerequisites

- DigitalOcean account
- Git repository access
- OpenAI API key
- Domain name (optional)

## Step 1: Create a Droplet

1. Login to your DigitalOcean account
2. Click "Create" → "Droplets"
3. Select options:
   - Ubuntu 22.04 LTS
   - Basic Plan ($5-10/month should be sufficient)
   - Choose a datacenter region close to your users
   - Add SSH key (recommended) or use password authentication
4. Click "Create Droplet"

## Step 2: Connect to Your Droplet

```bash
ssh root@your-droplet-ip
```

## Step 3: Update System and Install Dependencies

```bash
# Update system packages
apt update && apt upgrade -y

# Install required packages
apt install -y python3 python3-pip python3-venv nodejs npm nginx 

# Install Node.js 16+ LTS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt install -y nodejs

# Verify installations
python3 --version  # Should be 3.9+
node --version     # Should be 16+
npm --version
```

## Step 4: Clone Repository

```bash
# Create directory for application
mkdir -p /var/www
cd /var/www

# Clone the repository
git clone https://github.com/yourusername/hello3.git
cd hello3
```

## Step 5: Set Up Backend

```bash
# Create and activate virtual environment
cd /var/www/hello3
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

## Step 6: Set Up Frontend

```bash
# Install frontend dependencies
cd /var/www/hello3/frontend
npm install

# Build production version
npm run build
```

## Step 7: Configure Services

### Create a systemd service for the backend:

```bash
cat > /etc/systemd/system/memory-agent-backend.service << EOF
[Unit]
Description=Memory Agent Backend
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/hello3/backend
ExecStart=/var/www/hello3/venv/bin/python app.py
Restart=always
Environment="PATH=/var/www/hello3/venv/bin:/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
EOF

# Start and enable the service
systemctl daemon-reload
systemctl start memory-agent-backend
systemctl enable memory-agent-backend
```

### Configure Nginx

```bash
# Create Nginx config
cat > /etc/nginx/sites-available/memory-agent << EOF
server {
    listen 80;
    server_name your-domain.com;  # Or your server IP

    location /api {
        proxy_pass http://localhost:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location / {
        root /var/www/hello3/frontend/build;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }
}
EOF

# Enable the site
ln -s /etc/nginx/sites-available/memory-agent /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default  # Remove default site

# Test Nginx configuration
nginx -t

# Restart Nginx
systemctl restart nginx
```

## Step 8: Set Up Firewall

```bash
# Allow SSH, HTTP, and HTTPS
ufw allow ssh
ufw allow http
ufw allow https
ufw enable
```

## Step 9: SSL with Let's Encrypt (Optional)

If you have a domain pointing to your server:

```bash
# Install Certbot
apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
certbot --nginx -d your-domain.com

# Certbot modifies your Nginx configuration automatically
```

## Step 10: Verify Deployment

1. Visit your domain or server IP in a browser
2. Test the chat functionality
3. Check logs if there are issues:
   ```bash
   journalctl -u memory-agent-backend -f
   ```

## Step 11: Update Application

When you need to update the application:

```bash
cd /var/www/hello3
git pull

# Update backend
cd backend
source ../venv/bin/activate
pip install -r requirements.txt
systemctl restart memory-agent-backend

# Update frontend
cd ../frontend
npm install
npm run build
```

## Troubleshooting

- **Backend service not starting**: Check logs with `journalctl -u memory-agent-backend`
- **Frontend not loading**: Ensure Nginx is configured properly and serving from the correct build directory
- **API calls failing**: Verify backend is running and Nginx proxy_pass is configured correctly