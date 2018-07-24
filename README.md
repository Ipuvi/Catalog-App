# Catalog-App
Project 2 - Udacity IoT Foundation Nanodegree


 # Catalog Web App
This web app is a project for the Udacity IoT Foundation Nanodegree Course.
This web app is a project for the Udacity (https://classroom.udacity.com/nanodegrees/nd501-iniot).

## About
This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## In This Repo
This project has one main Python module `project.py` which runs the Flask application. A SQL database is created using the `databasetup.py` module and you can populate the database with test data using `CatalogData.py`.
The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. CSS/JS/Images are stored in the static directory.
 
 ## Skills Honed
 1. Python
 This web app is a project for the Udacity IoT Foundation Nanodegree Course.
 4. OAuth2.0
 5. Flask Framework
 
# Installation
 There are some dependancies and a few instructions on how to run the application.
Initially, install the vagrant, virtual box, and then clone the FSND vagrant file as it contains all setups preinstalled, then start running project.py files , as per the guidelines below...
 
To get the Google login working there are a few additional steps:
   - Rename JSON file to client_secrets.json
   - Place JSON file in item-catalog directory that you cloned from here
 
 1. Install Vagrant and VirtualBox
 2. Clone the fullstack-nanodegree-vm
 3. Launch the Vagrant VM (vagrant up)
 4. Write your Flask application locally in the vagrant/catalog directory (which will automatically be synced to /vagrant/catalog within the VM).
 5.Run your application within the VM (python /vagrant/catalog/application.py)
      Access and test your application by visiting http://localhost:8000 locally


## JSON Endpoints

The following are open to the public:


Catalog JSON: `/catalog/categories/JSON`
   Displays the whole catalog.

Categories JSON: `/catalog/categories/<int:category_id>/list/JSON`
   Displays list of specific categories

Category Items JSON: `/catalog/categories/<int:category_id>/list/<int:list_id>/JSON`
    Displays items of list for a specific category

Category Item JSON: `/catalog/categories/<int:category_id>/list/<int:list_id>/items/<int:item_id>/JSON`
    Displays a specific item.
