1. Open Xampp Control Panel. Start Apache and MySQL

2. Run these commands to grant privileges

create user 'DocV'@'localhost' identified by 'DocV_password';

grant all privileges on *.* to 'DocV'@'localhost';

3. Delete all the migration and pycache files (If already present). Drop the tables too.

4. Make migrations for all the apps

python manage.py makemigrations appname

(Here we have 5 apps : home, predict_heart, predict_cancer, predict_kidney, predict_diabetes)

5. python manage.py migrate 

6. Collect the static content

python manage.py collectstatic

7. Then create a superuser

python manage.py createsuperuser

8. Run the server

python manage.py runserver
