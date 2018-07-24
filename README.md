# Catalog-App
Project 2 - Udacity IoT Foundation Nanodegree


 # Item Catalog Web App
-This web app is a project for the Udacity IoT Foundation Nanodegree Course.
+This web app is a project for the Udacity (https://classroom.udacity.com/nanodegrees/nd501-iniot).
+
+## About
+This project is a RESTful web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.
+
+## In This Repo
+This project has one main Python module `project.py` which runs the Flask application. A SQL database is created using the `databasetup.py` module and you can populate the database with test data using `CatalogData.py`.
+The Flask application uses stored HTML templates in the tempaltes folder to build the front-end of the application. CSS/JS/Images are stored in the static directory.
 
 ## Skills Honed
 1. Python
@@ -8,7 +15,7 @@ This web app is a project for the Udacity IoT Foundation Nanodegree Course.
 4. OAuth2.0
 5. Flask Framework
 
-# Installation
+## Installation
 There are some dependancies and a few instructions on how to run the application.
+Initially, install the vagrant, virtual box, and then clone the FSND vagrant file as it contains all setups preinstalled, then start running project.py files , as per the guidelines below...
 
@@ -49,3 +56,18 @@ To get the Google login working there are a few additional steps:
 12. Rename JSON file to client_secrets.json
 13. Place JSON file in item-catalog directory that you cloned from here
 14. Run application using `python Catalog-App project.py`
+
+## JSON Endpoints
+The following are open to the public:
+
+Catalog JSON: `/catalog/categories/JSON`
+    - Displays the whole catalog.
+
+Categories JSON: `/catalog/categories/<int:category_id>/list/JSON`
+    - Displays list of specific categories
+
+Category Items JSON: `/catalog/categories/<int:category_id>/list/<int:list_id>/JSON`
+    - Displays items of list for a specific category
+
+Category Item JSON: `/catalog/categories/<int:category_id>/list/<int:list_id>/items/<int:item_id>/JSON`
+    - Displays a specific item.