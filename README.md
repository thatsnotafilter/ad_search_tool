# ad_search_tool
Django based MS Active Directory search tool

A single, google search form inspired, web page to search for any objects in your local MS Active Directory. 
- display quick information per search result and detailed information by clicking the search result
- responsive HTML template for big and small screens
- LDAPS

Technologies used: Python, Django (Python Web Framework) module, LDAP3 module and W3 CSS framework
- https://www.python.org/
- https://docs.djangoproject.com
- https://ldap3.readthedocs.io
- https://www.w3schools.com/w3css/

PREREQ:
- basic knowledge of Python, Django and Active Directory
- Python 3.6+
- Python modules Django (2+) and LDAP3 (2+)

HOW TO RUN:
- create django project (django-admin.py startproject adsearch)
- copy provided files to your django project folder (overwrite as needed)
- modify adsearch/settings.py AD related lines at the bottom to match your AD environment
- run django server (python manage.py runserver 0.0.0.0:8000)
- access the site from the host http://localhost:8000
