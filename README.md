# How To's
This Project consists of a collection of Web Applications that allow you to manage, edit and view How To's in the form of Step-By-Step procedures. An important key aspect is the modularity of the documentation. Reusable steps, pictures, explanations, links and so on are a core concept and the database is designed with that in mind.

The project documentation is done in the [Core API Repository](https://github.com/tiveritz/how-tos-api)

#### [Core API](https://github.com/tiveritz/how-tos-api)
The REST API that handles all database interactions on the documentation database.

#### [Administration](https://github.com/tiveritz/how-tos-administration)
A Website that allows users to manage the content. Consumes the Core API.

#### [Viewer](https://github.com/tiveritz/how-tos-viewer)
A Website that allows users to view the How To's. Consumes the Core API.

# Administration
The How To's Administration is a Python powered Website on the Django Framework.

URL: [https://ht.tiveritz.at](https://ht.tiveritz.at/)

### Dependencies
Django==3.1.4
python-dotenv==0.17.0 #for environment variables in settings.py
mysqlclient==2.0.3 #for database connection
requests==2.25.1 #for consuming the core API
