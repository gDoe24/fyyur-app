# Fyyur

Fyyur is a website used to facilitate bookings between musical venues and artists where venues can find talent in their area to play at their shows and vis versa. This site allows you to list venues, artists, and set up shows as the venue owner.

## Getting Started

**1. Backend Dependencies**

Our tech stack includes the following:

- Python3 and Flask as our server language and server framework
- SQLAlchemy ORM
- PostgreSQL as our database of choice
- Flask-Migrate for creating and running schema migrations 
- You can download and install the dependencies mentioned above using pip as:

```
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

**2. Frontend Dependencies**

If you have not already, download and install [Node.js](https://nodejs.org/en/download/). This is necessary to install Bootstrap 3.

Once you have downloaded Node.js, install Bootstrap 3:

```
npm init -y
npm install bootstrap@3
```

**3. Install Dependencies**

Install the remaining dependencies using:

```
npm init -y
npm install bootstrap@3
```

**4. Running the app**

Lastly, to run the app set your flask environment to app.py and run:

```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
