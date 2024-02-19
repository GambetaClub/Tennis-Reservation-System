# Tennis Club Reservation System
Welcome to the Tennis Club Reservation System! This web application is designed to facilitate reservations for tennis courts, manage events, handle user management, and provide a seamless experience for both club members and administrators.

## Features
User Management: Easily create, update, and delete user accounts. Users can register, log in, and manage their profiles.
Court Reservation: Members can reserve tennis courts for specific dates and times.
Event Management: Organize events such as tournaments, social gatherings, or coaching sessions.
Recurrent Events: Schedule recurring events on specific dates and times.
Calendar View: Visualize court availability and scheduled events on an interactive calendar.
Coach Capability: Assign coaches to events or sessions, allowing members to book coaching sessions.
## Installation
To run this application locally, make sure you have Docker installed on your system.

#### Clone this repository to your local machine:

```bash
git clone https://github.com/your/repository.git
```
#### Navigate to the project directory:

```bash
Copy code
cd tokeneke
```
#### Build the Docker image:
```bash
docker-compose build
```
#### Start the Docker containers:
```bash
docker-compose up
```
Access the application in your web browser at http://localhost:8000.

## Usage
Once the application is running, you can access the following endpoints:

/admin: Access the Django admin panel to manage users, events, courts, and other data.
/accounts: User authentication and profile management.
/events: View, create, and manage events.
/reservations: Make and manage court reservations.
/calendar: Visualize court availability and scheduled events.

### Dependencies
This application is built with Django, and PostgreSQL as the database backend. Additional dependencies can be found in the requirements.txt file.

### Configuration
You can customize the application settings by modifying the .env file. Here are some common configurations:

DEBUG: Set to True to enable debug mode.
SECRET_KEY: Secret key used for cryptographic signing.
DATABASE_URL: URL for connecting to the PostgreSQL database.
ALLOWED_HOSTS: List of allowed hosts for the application.

## Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository, make your changes, and submit a pull request.

Feel free to reach out to the project maintainers for any questions or support.
