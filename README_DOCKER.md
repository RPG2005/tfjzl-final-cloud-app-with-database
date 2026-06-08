# Docker para `tfjzl-final-cloud-app-with-database`

Este proyecto es una aplicación Django llamada `onlinecourse`.

## 1. Arrancar con Docker

Desde la carpeta donde está `manage.py`, ejecuta:

```bash
docker compose up --build
```

La aplicación quedará disponible en:

```text
http://localhost:8001/onlinecourse/
```

El panel de administración estará en:

```text
http://localhost:8001/admin/
```

> El contenedor escucha internamente en el puerto `8000`, pero se publica en tu equipo como `8001` para no chocar con otros proyectos Django.

## 2. Crear superusuario

Con el contenedor arrancado, abre otra terminal y ejecuta:

```bash
docker compose exec onlinecourse python3 manage.py createsuperuser
```

Ejemplo del laboratorio:

```text
Username: admin
Email: pulsa Enter
Password: p@ssword123
```

## 3. Parar el proyecto

```bash
docker compose down
```

## 4. Si quieres usar el puerto 8000 en tu equipo

Edita `docker-compose.yml` y cambia:

```yaml
ports:
  - "8001:8000"
```

por:

```yaml
ports:
  - "8000:8000"
```

## 5. Notas

Se ha ajustado `ALLOWED_HOSTS = ['*']` en `myproject/settings.py` para que funcione correctamente desde Docker o Cloud IDE.

El comando de arranque ejecuta automáticamente:

```bash
python3 manage.py makemigrations onlinecourse
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```
