# Restaurants
 
 ## Description:
 This is an app which is connected to  a databse with restaurants and menue 
 items for each restaurant. The app is based on *Flask* (witch is a microframework 
 for Python). Using this app we can ADD, REMOVE, UPDATE, and DELETE  restaurants names. 
 
   ## Installation:
 1. This project runs on pyhon2, Flask, and sqlAlchemy on ubuntu viraual env.(I highly 
 recomend to use vagrant and to run vagrant up using Vagrantfile from the project. 
 It will install all dependencies. 
 If you have vagrant up and running you can ignore step 5. To have success installing
 VM on your coumputer visit: 1. *www.virtualbox.org* 2. *www.vagrantup.com*.)
 2. **apt-get update**
 3. **apt-get install git-core**
 4. **git clone https://github.com/airdenis/restaurantmenu_flask.git**
 5. **pip install -r requirements.txt**
 6. In order to create restaurants database run **python database_setup.py**
 7. To populate database with some restaurants names run **python lotsofmenues.py**
 8. run **python project.py** to launch the app.
 9. open any browser on your computer **localhost:5000/restaurants** or **localhost:5000**.

