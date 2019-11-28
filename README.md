# cs50w-music

WIP  
My final project for CS50w - knockoff Spotify - a web application built with Django, DRF and React

backend is sort of complete

## setup  
`python3 -m venv env`  
`source env/bin/activate`  
`pip install -r requirements.txt`  
`python manage.py migrate`  

## run
`python manage.py runserver`  

## Endpoints  

### Home page
* GET /  
TODO

### User Endpoints  
* GET /api/users/  
Retrieve a list of all users.  

* GET /api/users/{id}/  
Retrieve details of a specific user.  

* PATCH /api/users/{id}/  
Modify details of a specific user. 

* DELETE /api/users/{id}/  
Delete a specific user. 

Django knox token authentication:

* POST /api/register/  
Register a new user.  

* POST /api/login/  
Log in and obtain an authentication token.  

* POST /api/logout/
Log out the current user.

* POST /api/logoutall/  
Remove all tokens that the server has - forcing all clients to re-authenticate

### Album Endpoints
* GET /api/albums/  
Retrieve a list of all albums.

* GET /api/albums/{id}/  
Retrieve details of a specific album.

* POST /api/albums/  
Create a new album.

* PATCH /api/albums/{id}/  
Update details of a specific album.

* DELETE /api/albums/{id}/  
Delete a specific album.

* POST /api/albums/{id}/manage_artists/  
Add an artist to the list of artists associated with an album.

* DELETE /api/albums/{id}/manage_artists/  
Remove an artist from the list of artists associated with an album.

### Song Endpoints
* GET /api/songs/  
Retrieve a list of all songs.

* GET /api/songs/{id}/  
Retrieve details of a specific song.

* POST /api/songs/  
Create a new song.

* PATCH /api/songs/{id}/  
Update details of a specific song.

* DELETE /api/songs/{id}/  
Delete a specific song.

* POST /api/songs/{id}/manage_artists/  
Add an artist to the list of artists associated with a song.

* DELETE /api/songs/{id}/manage_artists/  
Remove an artist from the list of artists associated with a song.

* GET /api/songs/{id}/play/  
Stream the audio file of a song.

### Playlist Endpoints
* GET /api/playlists/  
Retrieve a list of all playlists.

* GET /api/playlists/{id}/  
Retrieve details of a specific playlist.

* POST /api/playlists/  
Create a new playlist.

* PUT /api/playlists/{id}/  
Update details of a specific playlist.

* DELETE /api/playlists/{id}/  
Delete a specific playlist.

* POST /api/playlists/{id}/manage_songs/  
Add a song to a playlist.

* DELETE /api/playlists/{id}/manage_songs/  
Remvoe a song from a playlist.

## Testing - CI
**.github/workflows/ci.yml** The github action workflow, triggered on push events, runs Django unit tests for the project, ensuring seamless and automated testing.  
`python3 manage.py test --settings=cs50w_music.settings_test`
