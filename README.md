# WIP cs50w-music

My final project for CS50w - knockoff Spotify - a web application built with Django, DRF and React

What makes this app unique is that a song/album can be associated with and managed by multiple artist profiles.

backend is sort of complete
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
base url http://127.0.0.1:8000/api/  

Authorization and api rate limiting are set for security measures.  
For now all endpoints besides register and login require authentication, which might change in the future.

### User Endpoints  
* GET users/  
Retrieve a list of all users.  

* GET users/{id}/  
Retrieve details of a specific user.  

* PATCH users/{id}/  
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

* DELETE users/{id}/  
Set the a specific user as inactive.

Django knox token authentication:

* POST register/  
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

* POST login/  
Log in and obtain an authentication token.  
    * **username**  
    * **password**  

* POST logout/
Log out the current user.

* POST logoutall/  
Remove all tokens that the server has - forcing all clients to re-authenticate

### Album Endpoints
* GET albums/  
Retrieve a list of all albums.

* GET albums/{id}/  
Retrieve details of a specific album.

* POST albums/  
Create a new album.
    * **title**   
    * release_date  
    
    The current user is added in the artists list.

* PATCH albums/{id}/  
Update details of a specific album.
    * title
    * release_date
    * cover_image

* DELETE albums/{id}/  
Delete a specific album.

* POST albums/{id}/request_artist/  
Request to add an artist to the list of artists associated with an album.
    * **aritst_id**

* DELETE albums/{id}/remove_requested_artist/  
Remove an artist from requested artists.
    * **aritst_id**

* POST albums/{id}/confirm_current_user_as_artist/  
Confirm to be added as an artist to the list of artists associated with an album.

* DELETE albums/{id}/remove_current_user_as_artist/  
Remove current user from the list of artists associated with an album.

* GET albums/{id}/get_image/  
Stream the cover image file of an album.  
(unused) (instead serve static files from media in development; CDN would be more appropriate in production)

### Song Endpoints
* GET songs/  
Retrieve a list of all songs.

* GET songs/{id}/  
Retrieve details of a specific song.

* POST songs/  
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


* PATCH songs/{id}/  
Update details of a specific song.

* DELETE songs/{id}/  
Delete a specific song.

* POST songs/{id}/request_artist/  
Request to add an artist to the list of artists associated with a song.
    * **aritst_id**

* DELETE songs/{id}/remove_requested_artist/  
Remove an artist from requested artists.
    * **aritst_id**

* POST songs/{id}/confirm_current_user_as_artist/  
Confirm to be added as an artist to the list of artists associated with a song.

* DELETE songs/{id}/remove_current_user_as_artist/  
Remove current user from the list of artists associated with a song.

* GET songs/{id}/play/  
Stream the audio file of a song.  
(unused) (instead serve static files from media in development; CDN would be more appropriate in production)

* GET songs/{id}/get_image/  
Stream the cover image file of a song.  
(unused) (instead serve static files from media in development; CDN would be more appropriate in production)


### Playlist Endpoints
* GET playlists/  
Retrieve a list of all playlists.

* GET playlists/{id}/  
Retrieve details of a specific playlist.

* POST playlists/  
Create a new playlist.
    * **title**

    The current user is set as the owner of the playlist and the timestamp created_at is set to now.

* PATCH playlists/{id}/  
Update details of a specific playlist.
    * title

* DELETE playlists/{id}/  
Delete a specific playlist.

* POST playlists/{id}/manage_songs/  
Add a song to a playlist.
    * **song_id**

* DELETE playlists/{id}/manage_songs/  
Remove a song from a playlist.
    * **song_id**

## Testing - CI
**.github/workflows/ci.yml** The github action workflow, triggered on push events, runs Django unit tests for the project, ensuring seamless and automated testing.  
`cd backend`
`python3 manage.py test --settings=cs50w_music.settings_test`
