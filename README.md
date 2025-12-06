# StockFolio

📈 A real-time stock trading simulation platform built with Django, featuring live stock prices, portfolio management, and trading capabilities.

🎯 Features

72+ Real Stocks - Live prices from major markets (AAPL, MSFT, GOOGL, TSLA, etc.)

Real-Time Data - Auto-updating prices every 30 seconds

Portfolio Management - Track your investments and performance

Watchlist - Monitor stocks you're interested in

Trading Simulation - Buy and sell stocks with real market prices

Transaction History - Complete record of all your trades

Email Notifications - Get notified about successful trades

Admin Dashboard - Comprehensive management interface

Responsive Design - Works on desktop and mobile

🚀 Quick Setup & Run
Prerequisites

Python 3.11+ installed

pip (Python package manager)

Easy Setup

Install dependencies:

pip install -r requirements.txt


Run database migrations:
python manage.py migrate


Create admin user:
python manage.py createsuperuser


Populate with stock data:
python manage.py populate_stocks


Start the application:
python manage.py runserver

Your application will be live at http://localhost:8000

🌐 Access Your Application
Main Application → http://localhost:8000
Admin Panel → http://localhost:8000/admin
API Health Check → http://localhost:8000/api/health/

✔ Use the superuser credentials created earlier.

💼 Using the Application
Register/Login
Browse stocks
Add stocks to watchlist
Perform simulated trades
Track your portfolio
Check transaction history

🏗️ Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django App    │    │   Stock APIs    │
│   (HTML/CSS/JS) │◄──►│   (Python)      │◄──►│   (yfinance)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite/PG)   │
                       └─────────────────┘

📊 Available Stocks
Tech: AAPL, MSFT, GOOGL, AMZN, META, TSLA, NVDA, NFLX
Finance: JPM, BAC, WFC, GS, MS, V, MA, AXP
Healthcare: JNJ, PFE, UNH, MRK, ABT, ABBV
Consumer Goods: KO, PEP, WMT, COST, MCD, NKE
ETFs: SPY, QQQ, IWM, VTI

Total 72+ real market stocks

🔧 Development
Local Development (without Docker)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_stocks
python manage.py runserver

Additional Commands
python manage.py populate_stocks --symbols AAPL MSFT GOOGL
python manage.py runserver --verbosity=2
python manage.py runserver 0.0.0.0:8080

🔗 API Endpoints

/api/stock/<symbol>/price/

/api/watchlist/update-prices/

/api/health/

/api/ready/

/api/alive/

🛠️ Tech Stack

Backend: Django 4.2

Language: Python 3.11+

Frontend: HTML, CSS, JavaScript, Bootstrap

Database: SQLite

Stock Data: yfinance

Caching: In-memory

📝 License

This project is open source and available under the MIT License.

🤝 Contributing

Fork

Create feature branch

Commit changes

Submit PR

🆘 Support

If you face issues:

pip install -r requirements.txt

python manage.py migrate

python manage.py populate_stocks

Check terminal logs

⚙️ DevOps Integration (Docker + Ansible + Nagios + Terraform)

This project includes a full DevOps setup inside the infra/ directory.

🐳 1. Docker + Ansible Cluster

📍 Location: infra/ansible

▶️ Spin up Ansible Master & Worker Nodes
docker compose up -d


This creates 3 containers:

Container Name	Purpose
ansible-master	Runs playbooks
ansible-node1	Worker node
ansible-node2	Worker node
▶️ Run Playbook
docker exec -it ansible-master bash
cd /home/ansible/ansible-work
ansible-playbook hello-world.yml


This will automatically:

Install Python & packages

Clone your Django project

Install requirements

Run migrations

Start Django server at 0.0.0.0:8000

📊 2. Nagios Monitoring System

📍 Location: infra/nagios

▶️ Start Nagios
docker compose up -d

▶️ Open Nagios Web UI

👉 http://localhost:8081

Login:

Username: nagiosadmin

Password: nagios

Nagios Monitors:

CPU Usage

Memory

Disk

Ping (node up/down)

HTTP Service (optional)

🔁 3. FINAL 7 STEPS YOU MUST FOLLOW EVERY TIME

These steps ensure your Ansible deployment always works, even after shutdown.

1️⃣ Go to Ansible folder
cd "C:\Users\Nitish Kumar\OneDrive\Desktop\Stock_market_Prediction\infra\ansible"

2️⃣ Start Ansible containers
docker compose up -d


This launches:

ansible-master

ansible-node1

ansible-node2

3️⃣ Copy required Ansible files into master container

Run from PowerShell:

docker cp inventory.ini ansible-master:/home/ansible/ansible-work/
docker cp ansible.cfg ansible-master:/home/ansible/ansible-work/
docker cp hello-world.yml ansible-master:/home/ansible/ansible-work/

✔ Why this is important?

Fixes missing inventory error

Fixes sudo password error

Fixes playbook not found

Permanent clean solution

4️⃣ Enter Ansible master container
docker exec -it ansible-master bash
cd /home/ansible/ansible-work
ls


You MUST see:

inventory.ini
ansible.cfg
hello-world.yml

5️⃣ Test nodes
ansible all -m ping


Expected:

node1 | SUCCESS => pong
node2 | SUCCESS => pong

6️⃣ Run deployment
ansible-playbook hello-world.yml


This will:

✔ Install Python
✔ Clone Stock Market App
✔ Install dependencies
✔ Run database migrations
✔ Start Django server on port 8000

7️⃣ Open your Django project

Open browser:

👉 http://localhost:8000

👉 http://127.0.0.1:8000


Happy Trading! 📈💰







