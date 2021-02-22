# Object-Seeker
An applpication that helps you find your belongings which you left somewhere

1) In order to run this program(django based), you need to have a virtual environment.
2) You need to have virtualenvwrapper and virtualenv libs for creation of a new virtual environment. You can do this by typing the command
   "pip3 install virtualenv" and "pip3 install virtualenvwrapper". 
3) You can create a virtual environment by using the command in "virtualenv environment_name" in cmd or any terminal in windows.
4) After creation of the virtual environment and activating the environment(i.e. use command "workon environment_name" if not activated)
   you need to use the command "python manage.py runserver" in order to start the services i.e. run the server locally on your system.
5) You will get an address something like "https://127.0.0.1:8000/", open the address. Automatically recording from the camera connected 
   to your system will start in order to store the data.
6) In order to find your object press 'q' to stop recording and type the name of your object(any one(same spelling) from the list object.names)
   and you will get the latest location in which your object was placed.
