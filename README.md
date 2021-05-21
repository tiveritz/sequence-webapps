# How To's
This Project consists of a collection of Web Applications that allow you to manage, edit and view How To's in the form of Step-By-Step procedures. An important key aspect is the modularity of the documentation. Reusable steps, pictures, explanations, links and so on are a core concept and the database is designed with that in mind.
[(https://github.com/tiveritz/how-tos-api]

The REST API that handles all database interactions on the documentation database.<br>
[Swagger API documentation](https://api.tiveritz.at)

### [Webapps](https://github.com/tiveritz/how-tos-webapps)
Webapplications that allow content management and a viewer for the users. Consume the Core API.

### Dependencies
Django==3.1.4<br/>
python-dotenv==0.17.0 #for environment variables in settings.py<br/>
mysqlclient==2.0.3 #for database connection<br/>
requests==2.25.1 #for consuming the core API<br/>
