

# Lista de funcionalidades
1. Importa los módulos necesarios y carga las variables de entorno a través del archivo .env.
2. Crea una conexión con Google Sheets y obtiene los valores de una hoja de cálculo.
3. Analiza los valores y los convierte en un diccionario.
4. Recorre los valores parseados y genera una lista que contiene solo la dirección IP y el nombre de cada cliente.
5. Se conecta a la API del Mikrotik.
6. Obtiene una lista de direcciones IP en la lista 'Suspendido' del Mikrotik.
7. Genera una lista de diccionarios con el ID, dirección IP y comentario para cada dirección IP en la lista 'Suspendido'.
8. Genera una lista de identificadores de dirección IP que coinciden con la lista de direcciones IP de los clientes de Google Sheets.
9. Si una dirección IP de un cliente no se encuentra en la lista de direcciones IP suspendidas, crea una nueva dirección IP con el nombre y la dirección IP del cliente en la lista 'Suspendido' del Mikrotik.
10. Recorre la lista de diccionarios y genera una lista de comentarios para cada dirección IP suspendida que coincide con las direcciones IP de los clientes de Google Sheets.
11. Agrega la fecha actual al comentario de cada dirección IP suspendida.
12. Recorre la lista de identificadores de dirección IP suspendidos y los reactiva (elimina la suspensión) en el Mikrotik.
13. Recorre la lista de comentarios de dirección IP suspendidos y edita el comentario correspondiente para agregar la fecha de suspensión.
14. Cierra la conexión con la API del Mikrotik.

# Código de conexión con Google Sheets y Mikrotik

Este código establece una conexión con la API de Google Sheets para obtener datos de una hoja de cálculo y, posteriormente, con la API de Mikrotik para realizar una acción en el firewall.

## Dependencias

- `routeros_api`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`
- `python-dotenv`

## Configuración de variables

Este código utiliza variables de entorno para configurar los siguientes parámetros:

- `KEY`: ruta al archivo JSON de credenciales de Google Sheets.
- `SPREADSHEET_ID`: ID de la hoja de cálculo de Google Sheets que se utilizará.
- `SPREADSHEET_NAME`: nombre de la hoja de cálculo de Google Sheets que se utilizará.
- `IP_MIKROTIK`: dirección IP del router Mikrotik.
- `USER_MIKROTIK`: usuario para acceder al router Mikrotik.
- `PASS_MIKROTIK`: contraseña para acceder al router Mikrotik.

Estas variables se cargan desde un archivo `.env`.

## Conexión con Google Sheets

Se establece la conexión con la API de Google Sheets y se obtienen los valores de la hoja de cálculo especificada en las variables de entorno. A continuación, se convierten los valores en un diccionario y se almacenan en la variable `DATA_PARSED`.

## Acción en Mikrotik

Se establece la conexión con la API de Mikrotik y se obtiene una lista de direcciones IP de la lista `SUSPENDIDO` del firewall.
Luego, se genera una lista de diccionarios que contienen el ID, la dirección IP y el comentario de cada dirección IP suspendida.

A continuación, se recorre la lista de direcciones IP obtenida desde Google Sheets y se verifica si cada dirección IP está presente en la lista de direcciones IP suspendidas.
Si la dirección IP no está en la lista, se agrega como nueva dirección IP suspendida en el firewall.

Luego, se genera una lista de diccionarios que contienen el ID y el comentario de cada dirección IP suspendida que coincida con la lista obtenida desde Google Sheets.
Se agrega una fecha a cada comentario y se guarda en la variable `comment_finally`.

Finalmente, se recorre la lista de IDs de las direcciones IP suspendidas que coinciden con la lista obtenida desde Google Sheets y se habilita cada dirección IP.
Luego, se recorre la lista de comentarios de las direcciones IP suspendidas que coinciden con la lista obtenida desde Google Sheets y se actualiza cada comentario con la fecha agregada anteriormente.
