# Guía de Instalación

## Pasos

#### 
1. Instalamos las dependencias del proyecto usando el comando
~~~
pip install -r requirements.txt
~~~ 

2. Luego creamos la base de datos en postgresql, los datos del usuario administrador y el nombre de la base de datos deben coincidir con los escritos en la app dentro del archivo settings


3. Generamos las migraciones, hay que estar dentro de la carpeta del proyecto, a la altura del archivo **manage.py** y ejecutamos los comandos 
~~~
python manage.py makemigrations
python manage.py migrate
~~~

4. Posteriormente creamos el super usuario para tener un asuario admin con el cual ingresar al blog
~~~
python manage.py createsuperuser
~~~

5. Levantamos el servidor
~~~
python manage.py runserver
~~~