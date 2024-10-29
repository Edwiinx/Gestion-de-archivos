import sys
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox

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
            self.conexion = mysql.connector.connect(
                host='localhost',
                database='game_shop',
                user='sigma',  # Usar el nuevo usuario
                password='12345'  # Contraseña del nuevo usuario
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
