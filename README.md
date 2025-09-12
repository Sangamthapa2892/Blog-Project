Project Name: Django Blog Platform

Description:
This is a professional-grade Django web application featuring custom user authentication, password reset flow, contact form with email integration, and filterable blog posts. Built with a focus on backend clarity, Dockerized deployment, and clean UI/UX.

Features:
- Custom login view with Bootstrap styling and toast alerts
- Password reset flow with branded email templates
- Contact form with email confirmation and database logging
- Filter tabs for blog posts (All, Recent, Popular)
- Responsive design with fixed footer and modal headers
- Docker and Docker Compose support for local development
- `.env` configuration for secrets and environment variables

Tech Stack:
- Django 5.2.5
- Python 3.11
- Bootstrap 5
- Docker & Docker Compose
- SQLite (default) or PostgreSQL (optional)
- GitHub for version control and portfolio presentation

Setup Instructions:
1. Clone the repository:
   git clone https://github.com/yourusername/your-repo-name.git

2. Create a virtual environment and install dependencies:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Create a `.env` file in the base directory:
   SECRET_KEY=your-secret-key
   DEBUG=True
   EMAIL_HOST_USER=your-email@example.com
   EMAIL_HOST_PASSWORD=your-email-password
   DEFAULT_DOMAIN=127.0.0.1:8000
or 
Copy `.env.example` to `.env` and fill in your credentials before running the project.

4. Run migrations and start the server:
   python manage.py migrate
   python manage.py runserver

5. Access the app at:
   http://127.0.0.1:8000/

Docker Setup:
- Build and run using:
  docker-compose up --build

Author:
Sangam Thapa  
Bachelor in Computer Applications  
Backend Developer | Django User
Kathmandu, Nepal

License:
This project is licensed under the MIT License.
