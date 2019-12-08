# WIP cs50w-music

My final project for CS50w - knockoff Spotify - a web application built with Django, DRF and React

What makes this app unique is that a song/album can be associated with and managed by multiple artist profiles.

backend is sort of complete  
static files are served from media in development; CDN server would be more appropriate in production  
frontend is WIP

## setup  
`python3 -m venv env`  
`source env/bin/activate`  
`pip install -r backend/requirements.txt`  
`python backend/manage.py migrate`  

`npm install --prefix frontend/`

## run
Run these in separate terminals  

`python backend/manage.py runserver`  

`npm start  --prefix frontend/`

## Frontend  
http://127.0.0.1:3000/  

## API Endpoints  
base url http://127.0.0.1:8000/ 

Authorization and api rate limiting are set for security measures.  

### User Endpoints  
* GET api/users  
Retrieve a list of all users.  

* GET api/users{id}/  
Retrieve details of a specific user.  

* PATCH api/users{id}/  
Modify details of a specific user. 
    * username  
    * old_password (required when changing the password)
    * password  
    * password_confirmation
    * first_name  
    * last_name  
    * email  
    * birth_date  
    * country

* DELETE api/users{id}/  
Set the a specific user as inactive - soft delete.

Django knox token authentication:

* POST api/register/  
Register a new user and obtain an authentication token.
    * **username**  
    * **password**  
    * **password_confirmation**
    * first_name  
    * last_name  
    * email  
    * birth_date  
    * country

    The response contains the authentication token.

* POST api/login/  
Log in and obtain an authentication token.  
    * **username**  
    * **password**  

* POST api/logout/
Log out the current user.

* POST api/logoutall/  
Remove all tokens that the server has - forcing all clients to re-authenticate

### Album Endpoints
* GET api/albums/  
Retrieve a list of all albums.

* GET api/albums/{id}/  
Retrieve details of a specific album.

* POST api/albums/  
Create a new album.
    * **title**   
    * release_date  
    
    The current user is automcatically added to the artists list.

* PATCH api/albums/{id}/  
Update details of a specific album.
    * title
    * release_date
    * cover_image

* DELETE api/albums/{id}/  
Delete a specific album.

* POST api/albums/{id}/manage_requested_artists/  
Request to add an artist to the list of artists associated with an album.
    * **aritst_id**

* DELETE api/albums/{id}/manage_requested_artists/  
Remove an artist from requested artists.
    * **aritst_id**

* POST api/albums/{id}/confirm_current_user_as_artist/  
Confirm to be added as an artist to the list of artists associated with an album.

* DELETE api/albums/{id}/remove_current_user_as_artist/  
Remove current user from the list of artists associated with an album.


### Song Endpoints
* GET api/songs/  
Retrieve a list of all songs.

* GET api/songs/{id}/  
Retrieve details of a specific song.

* POST api/songs/  
Create a new song.
    * **title**  
    * **audio_file**  
    * release_date  
    * genre
    * album_id
    * duration (in seconds)
    * track_number (In the album)
    * cover_image
    
    The current user is added in the artists list.


* PATCH api/songs/{id}/  
Update details of a specific song.

* DELETE api/songs/{id}/  
Delete a specific song.

* POST api/songs/{id}/manage_requested_artists/  
Request to add an artist to the list of artists associated with a song.
    * **aritst_id**

* DELETE api/songs/{id}/manage_requested_artists/  
Remove an artist from requested artists.
    * **aritst_id**

* POST api/songs/{id}/confirm_current_user_as_artist/  
Confirm to be added as an artist to the list of artists associated with a song.

* DELETE api/songs/{id}/remove_current_user_as_artist/  
Remove current user from the list of artists associated with a song.


### Playlist Endpoints
* GET api/playlists/  
Retrieve a list of all playlists.

* GET api/playlists/{id}/  
Retrieve details of a specific playlist.

* POST api/playlists/  
Create a new playlist.
    * **title**

    The current user is set as the owner of the playlist and the timestamp created_at is set to now.

* PATCH api/playlists/{id}/  
Update details of a specific playlist.
    * title

* DELETE api/playlists/{id}/  
Delete a specific playlist.

* POST api/playlists/{id}/manage_songs/  
Add a song to a playlist.
    * **song_id**

* DELETE api/playlists/{id}/manage_songs/  
Remove a song from a playlist.
    * **song_id**


### Notification Endpoints (django-notifications app)
* GET notifications/api/all_list/  
List all unread notifications
    * max  
    * mark_as_read

* GET notifications/api/unread_list
List all notifications
    * max  
    * mark_as_read

* GET notifications/api/unread_count/
Get the count of the unread notifications


## Testing - CI
**.github/workflows/ci.yml** The github action workflow, triggered on push events, runs Django unit tests for the project, ensuring seamless and automated testing.  
`cd backend`  
`python3 manage.py test --settings=cs50w_music.settings_test`
