"""Conexión centralizada a PostgreSQL para Jorge Tech."""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def obtener_url_conexion():
    """Obtiene la URL sin exponer credenciales en el repositorio."""
    return os.environ.get("DATABASE_URL") or (
        "host={host} port={port} dbname={database} user={user} password={password}".format(
            host=os.environ.get("PGHOST", "localhost"),
            port=os.environ.get("PGPORT", "5432"),
            database=os.environ.get("PGDATABASE", "jorge_tech"),
            user=os.environ.get("PGUSER", "postgres"),
            password=os.environ.get("PGPASSWORD", ""),
        )
    )


def obtener_conexion():
    """Abre una conexión con filas tipo diccionario para usar en Jinja2."""
    return psycopg.connect(obtener_url_conexion(), row_factory=dict_row)


def probar_conexion():
    """Comprueba la conexión sin cambiar datos."""
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT 1 AS conexion_ok")
        correcto = cursor.fetchone()["conexion_ok"] == 1
        cursor.close()
        conexion.close()
        return correcto, "Conexión a PostgreSQL correcta."
    except psycopg.Error as error:
        return False, str(error)


def inicializar_esquema():
    """Crea las tablas y datos de ejemplo si todavía no existen.

    Render ejecuta la aplicación con DATABASE_URL. Esta función permite que una
    instancia nueva cree la estructura desde sql/esquema.sql sin guardar
    contraseñas en el repositorio.
    """
    ruta_esquema = Path(__file__).resolve().parent.parent / "sql" / "esquema.sql"
    contenido = ruta_esquema.read_text(encoding="utf-8")
    # El archivo usa comentarios SQL; se retiran antes de separar instrucciones.
    contenido_sin_comentarios = "\n".join(
        linea for linea in contenido.splitlines() if not linea.lstrip().startswith("--")
    )
    sentencias = [sentencia.strip() for sentencia in contenido_sin_comentarios.split(";") if sentencia.strip()]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        for sentencia in sentencias:
            cursor.execute(sentencia)
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        cursor.close()
        conexion.close()
