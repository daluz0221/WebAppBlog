# Uso de la AppWeb

##### 1. Después de de haber hecho la instalación, ingresamos al blog mediante la url localhost:8000 

##### 2. en la app, inicialmente no se mostraran los blogs, puesto que la base de datos está vacía, por lo que deberemos ingresar con el usuario administrador para crear algunos blogs y categorias

##### 3. Ingresamos a la url **localhost:8000/accounts/login/**, entramos con nuestro usuario administrador, ubicamos en la parte superior derecha el boton "ver perfil" e ingresamos a la zona administrativa 

##### 4. una vez en el área administrativa, le damos en el boton "Crear nueva categoria", para que cuando se vayan a crear los post no tengamos problemas.

##### 5. Una vez con algunas categorias creadas, ya podemos crear algunos post

# Dependencias

## Realmente dependencias de terceros  se usaron varias, 2  las cuales ayudaban a mejorar la parte visual de la aplicación

 1. django-ckeditor, esta dependencia se encarga de que el campo TextField de los modelos Post y Comment tengan más opciones de perzonalización del texto que se le ofrece al usuario

    importamos lo siguiente
    ~~~
    from ckeditor.fields import RichTextField
    ~~~
    y lo agregamos a los campos deseados
    ~~~
    body = RichTextField(blank=True, null=True)
    ~~~


 2. django-crispy-forms, esta dependencia se encarga de aplicar estilos css (puede ser de bootstrap o fundation), para usarlo debemos agregar en nuestro archivo settings.py en la lista de installed_apps lo siguiente "crispy_forms" y mas abajo, fuera de las installed_apps el siguiente código

    ~~~
    CRISPY_TEMPLATE_PACK = 'bootstrap4'
    ~~~

    luego en los templates en donde lo queramos usar, colocamos arriba 
    ~~~
    {% load crispy_forms_tags %}
    ~~~

    luego decoramos el formulario deseado
    ~~~
    {{form|crispy}}
    ~~~

3. psycopg2, depencia que nos facilita la conexión con postgresql, para instalarla solo debemos usar el comando
    ~~~
    pip install psycopg2
    ~~~
    sin embargo, si estamos corriendo el proyecto en linux debemos usar
    ~~~
    pip install psycopg2-binary
    ~~~

    ## Al momento de registrar un usuario, después de llenar el formulario de registro, se le envía al usuario un código de verificación para activar la cuenta, para fines prácticos se usó la consola para imprimir estos correos