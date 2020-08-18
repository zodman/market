# market

[![Coverage Status](https://coveralls.io/repos/github/zodman/market/badge.svg?branch=master)](https://coveralls.io/github/zodman/market?branch=master)

![Django CI](https://github.com/zodman/market/workflows/Django%20CI/badge.svg?branch=master)


# Plan

code of project 16hrs

* Code
    * Admin
    * Defining Models
    * CartBasket
* Unittest
* Provision & CI
* Documentation


# The admin

The django admin had 3 catalogs:

Food, Cart, Order

Demo: http://market.python3.ninja


# Main tools used:

* django-restframework
* inertia-django
* @inertia/vuejs
* parcel
  
More details on [requirements.in](requirements.in) and
[package.json](package.json)


# Populate the database with foods

`python populate.py`

# Install
Create a virtualenv

`pip install -r requirementst.xt`

Init the database:

`fab reinit`

Admin password is: admin 

To execute the unittes:

`fab test`

# Run on the web

First load your virtualenv

The part of the fronted runs & runserver with:

```
$ npm install
$ npm run dev
```
This will fire concurrently the parcel watch and runserver 


visit http://localhost:8000/


