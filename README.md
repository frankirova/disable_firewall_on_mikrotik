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
