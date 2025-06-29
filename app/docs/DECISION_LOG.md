## Technical Decisions

### 1. Python Version
- **Python 3.12**     : Elegido por su facilidad de uso en entornos de desarrollo

### 2. FastAPI
- **FastAPI**         : Elegida para generar APIs RESTful
- **uvicorn**         : Elegida para el servidor de desarrollo 

### 3. docker compose
- **docker compose**      : Elegida para la gestion de contenedores y servicios que permiten la creacion de entornos de desarrollo seguros y estables
- **Multi-stage Build**   : para crear una imagen de produccion mas pequeña
- **Health Checks**       : script en el docker compose para verificar que la base de datos esta lista para recibir peticiones.
- **Network**             : para comunicar la base de datos con el contenedor de la aplicacion y/o entre contenedores.
- **Volume**              : para persistir los datos de la base de datos.

### 4. Database Choice
- **MySQL**               : Elegida por su estabilidad y gestion de datos eficientes y seguros
- **SQLModel**            : Combina SQLAlchemy ORM con Pydantic validation
- **Connection Pooling**  : Implementado con SQLAlchemy para conexiones eficientes.
- **sqlite3**             : para pruebas integrales y aislar la base de datos principal.
 
### 5. Authentication & Authorization
- **bcrypt**                : Implementacion de encriptacion de contraseñas
- **JWT Implementation**    : Implementacion de tokens para la gestion de sesiones
- **Protected Routes**      : Implementacion de rutas protegidas para endpoints sensibles

### 6. Testing
- **pytest**              :   Test runner con objetivo de testear la funcionalidad de la aplicacion
- **test unitarios**      :   Test unitarios para testear la funcionalidad de la aplicacion con mock data 
- **test integracion**    :   Test integracion para testear la funcionalidad de la aplicacion con datos reales usando sqlite3 para la base de datos

### 7. Error Handling
- **Custom Exceptions**   : Manejo de errores personalizados
- **HTTP Exception Mapping**: Conversion de errores de dominio a códigos HTTP


