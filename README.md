# Flask Video API

This is a simple **Flask-RESTful** API to manage video data. The API allows you to perform CRUD operations on video information, including video name, views, and likes. The data is stored in a **SQLite** database.

## Features

- **Create** a new video.
- **Read** video details by ID.
- **Update** video details (name, views, likes).
- **Delete** a video by ID.
- View all available videos.

## Technologies Used

- **Flask** - A lightweight Python web framework.
- **Flask-RESTful** - An extension for Flask to easily build REST APIs.
- **SQLAlchemy** - ORM (Object Relational Mapper) for interacting with the SQLite database.
- **SQLite** - A simple, serverless SQL database for storing video data.

## Setup and Installation

### Prerequisites

Ensure you have Python 3.x and `pip` installed.

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/Rog3rinS/flask-video-api.git
   cd flask-video-api

2. Create and activate a virtual enviroment:
   
   ```bash
    python3 -m venv venv
    source venv/bin/activate  

**Setting Up the Database**
1. To set up the database, run the following command to create the necessary tables:
python

   ```bash
    from app import db
    db.create_all()
