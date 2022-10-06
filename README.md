# Trabajo Práctico Individual Sistemas Distribuidos 1 (FIUBA)
 
En este repositorio se encuentra el trabajo práctico individual de la materia Sistemas Distribuidos de la Facultad de Ingeniería de Buenos Aires.
 
Dentro del repositorio se encontraran distintas carpetas
 
## Sistema
 
El sistema estará compuesto por varios servicios que proveen la funcionalidad pedida
 
- Middleware
- Ingestion Service
- Like Filter
- Funny Filter
- Trending Filter
- Day Grouper
- Max
- Reporting/Storage Service
 
## Cliente
 
Dentro del cliente se encuentra un script en Python para procesar los videos en formato csv y enviarlos al sistema.
A su vez se encuentran las siguientes carpetas
 
### Videos
 
Videos a procesar
 
### VideosDev
 
Videos a procesar (orientados a pruebas y desarrollo)
 
### Categories
 
Categorias de los videos
 
### Thumbnails
 
Aqui se guardaran los thumbnails descargados
 
## Dependeces
Se provee un módulo `dependences` con todo código o lógica compartida que puede reutilizarse tanto en el cliente como en el sistema.
 
## Middleware Clients
Para la comunicación cliente - servidor y entre servicios, se proveen dos módulos para encapsular la lógica de comunicación
 
- middleware_client
- middlewaresys_client
 
## Herramientas
Se proveen los siguientes scripts de ejecución
 
```
`build.sh` -> Buildea las dependencias
`create_compose.sh` -> Construye el docker-compose para levantar el entorno
`up.sh` -> Levanta el entorno de docker
`run.sh` -> Corre el cliente
`stop.sh` -> Detiene entornos de docker (cliente y sistema)
`logs.sh` -> Obtiene los logs de los contenedores involucrados
```
 
## Utilización
 
Para correr el entorno primero ejecutar
 
```
./create_compose.sh ${NUMERO_DE_INSTANCIAS}
```
 
Lo cual generará el docker-compose con la cantidad de instancias de los servicios deseadas
 
Luego, de ser necesario, construir las imágenes base utilizando.
 
```
./build.sh
```
 
Posteriormente se puede ejecutar
```
./run_all.sh
```
 
El cual ejecutará los scripts de inicialización y frenado de entornos