# -*- encoding: utf-8 -*-

#importamos librerias necesarias
import MySQLdb

#datos para la conexion a la base de datos """ OJO CAMBIAR LOS DATOS POR LOS DE SU BD"""
BD_HOST = 'localhost'
BD_USUARIO = 'root'
BD_PASSWORD = 'test'
BD_NOMBRE = 'inventario'

#funcion para realizarconsulta
def consultas (consulta):
    #los datos se agregan a una lista
    datos_conexion = [BD_HOST, BD_USUARIO, BD_PASSWORD, BD_NOMBRE]
    #conectamos a la BD
    conn = MySQLdb.connect(*datos_conexion, charset = 'utf8')
    #creamos un cursor
    cursor = conn.cursor()
    #ejecutamos una consulta
    cursor.execute(consulta)
    #segun yo checa si la primera palabra del la consulta el select
    if consulta.startswith("SELECT"):
    #realiza la consulta y lo almacena en datos
        datos = cursor.fetchall()
    #si no es select hace las modificaciones a la BD
    else:
    #hace efectiva la escritura de los datos
        conn.commit()
    #datos se vuelve en nada
        datos = None
    #cerramos el cursor
    cursor.close()
    #cerramos la conexion
    conn.close()
    #regresamos la variable datos
    return datos
