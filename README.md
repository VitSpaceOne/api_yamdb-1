# api_yamdb
This project I've created during the course with the toy team of two developers. As a toy teamlead I described and separated tasks between developers, made architectural decision and defended the project during review. About 50% of code is written by me. I fully wrote users app, but I also contributed a lot to api app.
Project contains three apps: reviews, api, users. reviews app implement models, api app implements access to models via api, users app implements all the logic that needed for user management and access: permissions, singup and token endpoints. Full description of endpoints and queries are available on /redoc/

## Run application locally
Create and activate virtual enviroment
In /api_yamdb/api_yamdb/ run commands:
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## users app
It the application implemented extended user model, permissions and API to users management for users as well as for admins.

### Roles
- Anonim — can get titles decriptions, reviews and comments
- Authenticated user (user) — as well as Anonim can get all and additionally can publish reviews and scores to titles, can comment another reviews. This role is granted by default
- Moderator — has same rights with authenticated user and additionally can delete any reviews and comments
- Admin — has full rights to manage a content. Can created and delete titles, cateogries, genres, can manage other users
- Django Superusers — has same rights with admin, but role can't be changed

### Endpoints

- /auth/singup/ — sign up new user
- /auth/token/ — retrieve token

Sign up and authentication algorithm:
1. User sends an email and user name using POST
2. Default Django PasswordResetTokenGenerator generates token, that sends to user's email. This token is required to retrieve JWT-token that is needed to send queries to base endpoints
3. The user sends username and token given on email using 'confirmation_code' field using POST and retrieves JWT-token if data is valid

- /users/ — users collection, handles all queries except PUT
- /users/me/ — endpoint for getting and managing data about yourself

## reviews app

### Models
The app implements models for API:
- Category - categories (types) of titles (ex: "Film", "Book", "Music");
- Genre - genres of titles, one title might be related with few genres;
- Title - specified titles, to which users write reviews (to film, book, song);
- Review - reviews to titles;
- Comment - comments to reviews;
- GenreTitle - additional model for implementing Title-Genre many-to-many relationship;

### Test data uploading
In the directory /api_yamdb/static/data are prepared .csv files with the test data could be used for resources
To upload test data run following command:
```
py manage.py convert_csv_to_sqlite
```
