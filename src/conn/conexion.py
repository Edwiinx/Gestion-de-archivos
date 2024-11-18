import sys
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox
import os

class ConexionDB(QWidget):
    def __init__(self):
        super().__init__()
        self.conexion = None  
        self.conectar_base_datos()  
        self.initUI()  

    def initUI(self):
        self.setWindowTitle('Conexión a Game Shop')
        self.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()

        if self.conexion:
            label = QLabel("Conexión exitosa a la base de datos 'game_shop'.")
        else:
            label = QLabel("Error al conectar a la base de datos.")

        layout.addWidget(label)
        self.setLayout(layout)

    def conectar_base_datos(self):
        try:
            # Ruta relativa al certificado SSL (asegúrate de tener el archivo en el directorio correcto)
            ssl_ca = os.path.join(os.path.dirname(__file__), 'sql/ssl/DigiCertGlobalRootG2.crt.pem')

            # Conexión a la base de datos Azure MySQL
            self.conexion = mysql.connector.connect(
                host='gameshop.mysql.database.azure.com',  # El nombre del servidor de Azure
                database='game_shop',
                user='sigma',  # Usuario de la base de datos en Azure
                password='Eskibiritoilet1*',  # Contraseña de la base de datos en Azure
                ssl_ca=ssl_ca,  # Ruta del certificado SSL
                ssl_verify_cert=False,  
                ssl_disabled=False    # Habilitar la verificación del certificado
            )

            if self.conexion.is_connected():
                print("Conexión exitosa a la base de datos.")
                return self.conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = ConexionDB()
    ventana.show()
    sys.exit(app.exec_())
