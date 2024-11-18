import mysql.connector
import os

#IMPORTANTE este archivo es para demostracion de como realizar la conexion a azure


# Datos de conexión
host = "gameshop.mysql.database.azure.com"
user = "sigma"  # Usuario proporcionado
password = "Eskibiritoilet1*"  #aseña del administrador
database = "game_shop"  # El nombre de la base de datos

# Ruta relativa al certificado SSL
ssl_ca = os.path.join(os.path.dirname(__file__), '../sql/ssl/DigiCertGlobalRootG2.crt.pem')

# Establecer la conexión con la base de datos
try:
    conexion = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        ssl_ca=ssl_ca,  # Ruta relativa del certificado
        ssl_verify_cert=False,  
        ssl_disabled=False  
    )
    print("Conexión exitosa")
    
    # Crear un cursor para ejecutar consultas
    cursor = conexion.cursor()
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print("Base de datos conectada:", result)

except mysql.connector.Error as err:
    print(f"Error: {err}")
    conexion = None  # Asegúrate de que conn esté definido en el caso de error

finally:
    if conexion:
        conexion.close()
