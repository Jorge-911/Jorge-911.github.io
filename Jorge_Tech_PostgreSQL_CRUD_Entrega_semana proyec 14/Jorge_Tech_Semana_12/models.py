"""Modelo de usuario compatible con Flask-Login."""
from flask_login import UserMixin
from psycopg import Error

from conexion.conexion import obtener_conexion


class Usuario(UserMixin):
    """Usuario autenticado; la contraseña se conserva como hash, nunca texto plano."""

    def __init__(self, usuario_id, nombre_usuario, password_hash):
        self.id = str(usuario_id)
        self.usuario = nombre_usuario
        self.password_hash = password_hash

    @classmethod
    def desde_fila(cls, fila):
        if fila is None:
            return None
        return cls(fila["id"], fila["usuario"], fila["password"])

    @classmethod
    def buscar_por_id(cls, usuario_id):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE id = %s", (usuario_id,))
            return cls.desde_fila(cursor.fetchone())
        finally:
            cursor.close()
            conexion.close()

    @classmethod
    def buscar_por_nombre(cls, nombre_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT id, usuario, password FROM usuarios WHERE usuario = %s", (nombre_usuario,))
            return cls.desde_fila(cursor.fetchone())
        finally:
            cursor.close()
            conexion.close()
