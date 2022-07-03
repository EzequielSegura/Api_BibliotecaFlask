#Crear la clase configuracion
class Config:
    pass
#Crear Configuracion 
class DevelopmentConfig(Config):
    DEBUG = True
    #Asignar usuario, contraseña y direccion de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/biblioteca'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
#Almacenar la configuracion en un diccionario para su posterior uso
config = {
    'development': DevelopmentConfig,
}