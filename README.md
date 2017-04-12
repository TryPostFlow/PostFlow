# PostFlow

PostFlow is A simple, powerful publishing platform.

## Feature

* Admin Interface
* Support Markdown
* Support Custom Theme
* Command Line Interface

## Quickstart

* Create a virtualenv
* Install dependencies and PostFlow
    * `make install`
* Initialize PostFlow
    * `postflow init`
* Run the development server
    * `make server run` or `postflow run`
* Visit home page [localhost:5000](http://localhost:5000) and admin panel [localhost:5000/admin](http://localhost:5000/admin)
* Run the Admin Panel in the development mode.
    * `make admin-serve`
* Visit the Admin Panel [localhost:8080](http://localhost:8080)
* Run PostFlow in the production mode. Default port is `8000`
    * `postflow start`