# ACCORDION RENTAL APP

#### Video Demo: <URL HERE>

## 👀 Description

The **Accordion Rental App** is a web-based platform that streamlines the rental process for musical instruments, focusing on accordions.

The Django admin panel provides tools for managing:

- User data
- Instruments
- Contracts
- Invoices
- Agreements

For Users:

- Guests
  Guests can browse available and rented instruments. Rented instruments are displayed with their expected return dates.
- Registered Users
  After registering, users can reserve instruments temporarily while deciding. Since rental rates are dynamic (based on the rental period), users are given a short decision window.

Once a rental agreement is submitted:

- A PDF agreement, generated in the user’s profile-selected language, is automatically emailed.
- Invoices are created based on the user’s language preference and chosen payment interval. New invoices are checked and emailed daily.

Users can view their contracts and invoices on their dashboard and download them as PDFs.

Before the rental period ends, an automated reminder is sent, prompting the user to coordinate with the lessor about either returning the instrument or extending the contract. If the admin does not mark the instrument as "returned," the agreement is extended automatically.

For Staff:
Users with "staff" status are redirected to an admin dashboard where they can:

- Track payments and upload bank statement XML files
- Send notifications,
- Update contract statuses (e.g., "digitally signed," "instrument returned").

Statuses can be updated manually using buttons on the interface.

Additional features for staff include:

- Sending short emails via a message form.
- Editing an "additional info" field.
- Sorting contracts by various fields for better tracking of payments due or advance payments.

## 👇 Key Features

- User Profiles:
  Users can register, log in, and manage their profiles.
- Instrument Management:
  Users can browse and reserve instruments, with real-time availability and pricing updates..
- Agreements and Invoices:
  Rental agreements and invoices are generated and sent automatically based on user preferences.
- Automate remainders:
  Notifications are sent to users before the end of their rental period, ensuring proactive communication.
- Admin Dashboard:
  Staff can manage contracts, update statuses, track payments, and send messages.
- Email Notifications:
  Custom email messages can be sent directly from the admin dashboard.
- JWT Authentication, csrf tokens:
  Ensures secure login and session management with access tokens.

## Project Structure

### Frontend (accordion-rental/frontend)

This folder contains the React application for the user interface.

#### Key Files:

- src/App.js
  Entry point for the React app; contains routes for various pages.
- src/components/AdminDashboard.js
  Admin panel with tools for managing contracts, sending emails, and updating information.
- src/components/ProfileForm.js
  User profile management form for updating personal information.
- src/components/InstrumentDetails.js
  Displays detailed instrument information and allows reservations.
- .env
  Configuration for API endpoint (e.g., VITE_API=192.168.1.187:8000).

### Backend (accordion-rental/backend)

This folder contains the Django project that powers the backend API.

#### Key Files:

- manage.py
  Entry point for the Django application.
- settings.py
  Configuration for the Django project, including installed apps, database, and authentication settings.
- urls.py
  Defines all API endpoints and routes.
- models.py
  Contains the data models for users, instruments, and agreements.
- views.py
  Handles requests and responses for the app's functionality, including contract updates and email notifications.
  serializers.py
  Serializes data between Django models and API responses.
- permissions.py
  Custom permissions for securing API endpoints.

#### Database (db.sqlite3)

SQLite database file storing user profiles, agreements, instruments, and other app data.

## 👩‍💻 Running the Project

### Prerequisites

- Python 3.12+
  Install Python from python.org.
- Node.js and npm
  Install Node.js from nodejs.org.
- SQLite
  SQLite is included with Python.

## Setup Instructions

#### Backend Setup

1. Navigate to the backend folder:

```bash
cd accordion-rental/backend
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations to set up the database:

```bash
python manage.py migrate
```

5. Start the Django server:

```bash
python manage.py runserver
```

#### Frontend Setup

1. Navigate to the frontend folder:

```bash
cd accordion-rental/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the React development server:

```bash
npm start
```

### Access the Application

- Frontend (React):
  Open your browser and go to http://localhost:3000.

- Backend (Django):
  API is accessible at http://localhost:8000/api/.

## Usage

1. Admin Tasks:

- Log in as an admin.
- View agreements and send email notifications.
- Update contract statuses (e.g., "Signed" or "Finished").

2. User Actions:

- Browse instruments and reserve them.
- Manage personal information via the profile form.

## Troubleshooting

1. Permission Errors with SQLite:

- Ensure the database file and directory have proper permissions:

```bash
chmod 664 backend/db.sqlite3
chmod 775 backend/
```

2. Frontend Fails to Connect to Backend:

- Verify the API URL in .env matches the backend server's IP and port.

3. Missing Dependencies:

- Run pip install and npm install to ensure all required packages are installed.

## References

Used forums: Stack Overflow, Reddit.
Sone parts of this code are created with assistance of OpenAI. (2024). ChatGPT (Version 4) language model

## License

Retaining all rights and control over distribution and usage.
Users are kindly asked getting contact before reuse, modification, or redistribution.
Feel free to contact if you want additional information.
