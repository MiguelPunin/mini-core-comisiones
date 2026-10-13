# Mini Core: Sistema de ventas y comisiones

Adaptación académica para la **Tarea 4: Aplicación Ejercicio MVC**, basada en un proyecto de semestres anteriores de la Universidad de las Américas (UDLA).

**Estudiante:** Miguel Punin ([MiguelPunin](https://github.com/MiguelPunin)).
**Asignatura:** Desarrollo Web, semestre 7.

La aplicación registra ventas y calcula comisiones por vendedor dentro de un rango de fechas. Esta adaptación incluye una interfaz clara con fondo crema, tarjetas blancas y acentos verdes, configuración de Render y PostgreSQL en la nube.

## Aplicación desplegada

| Recurso | Enlace |
|---|---|
| Frontend | [Abrir aplicación](https://mini-core-frontend.onrender.com) |
| Backend | [Abrir API](https://mini-core-backend-x00b.onrender.com/api/) |
| Repositorio | [mini-core-comisiones](https://github.com/MiguelPunin/mini-core-comisiones) |

El backend define `/api/` y `/admin/`. Entrar en `/` o `/docs` devuelve 404. El servicio gratuito puede tardar en responder después de un período de inactividad.

## Funcionalidades

- Crear, listar y eliminar ventas desde la interfaz.
- Mostrar la comisión de cada venta.
- Filtrar reportes por fecha de inicio y fin, ambas incluidas.
- Mostrar totales y detalle de ventas y comisiones por vendedor.

La API también permite administrar vendedores y reglas y actualizar ventas; estas opciones no tienen formularios en el frontend actual.

## Arquitectura

| Capa | Tecnologías | Responsabilidad |
|---|---|---|
| Backend | Python 3.11, Django 4.2, Django REST Framework | API, validación y comisiones |
| Frontend | React 19, Vite 6, Axios, date-fns | Interfaz y consumo de JSON |
| Datos | SQLite local / PostgreSQL en Render | Persistencia |
| Despliegue | Render, Gunicorn, WhiteNoise | Servicios y estáticos de Django |

En relación con MVC, los modelos de Django representan los datos y contienen el cálculo de comisión. Las vistas de `views.py` manejan las peticiones y generan JSON. React presenta los resultados. Aunque Django suele describirse mediante MVT, esta aplicación utiliza React para su interfaz en lugar de templates de Django.

## Archivos principales

| Archivo | Función |
|---|---|
| `backend/commission_app/models.py` | Vendedor, Regla, Venta, ComisionCalculada y cálculo |
| `backend/commission_app/serializers.py` | JSON y validación de fechas |
| `backend/commission_app/views.py` | Endpoints, filtros y agrupación por vendedor |
| `backend/commission_app/urls.py` | Rutas de la API |
| `backend/commission_app/fixtures/initial_data.json` | Datos de ejemplo |
| `backend/commission_app/management/commands/seed_demo.py` | Carga inicial sin sobrescribir datos existentes |
| `backend/commission_project/settings.py` | Base de datos, CORS y estáticos |
| `backend/build.sh` | Instalación y collectstatic |
| `frontend/src/App.jsx` | Formulario, tabla y reporte |
| `frontend/src/services/api.js` | Cliente Axios y URL del backend |
| `frontend/src/services/commissionService.js` | Peticiones a la API |
| `frontend/src/App.css` e `index.css` | Estilos |

## Ejecución local en Windows (PowerShell)

Requisitos: Python 3.11 y Node.js con npm (Node 22 recomendado). Mantener dos terminales abiertas.

### Backend

```powershell
git clone https://github.com/MiguelPunin/mini-core-comisiones.git
cd mini-core-comisiones
python -m venv .venv
cd backend
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py seed_demo
..\.venv\Scripts\python.exe manage.py runserver
```

El entorno `.venv` queda en la raíz; estos comandos no requieren activarlo. API local: http://127.0.0.1:8000/api/.

`seed_demo` carga cuatro vendedores, cuatro reglas y cinco ventas únicamente si las tablas de vendedores, reglas y ventas están vacías. Las ventas de ejemplo son de mayo y junio de 2025: seleccionar ese período para verlas en los reportes.

### Frontend

En otra terminal, desde la raíz del proyecto:

```powershell
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Abrir http://127.0.0.1:3000/. Axios apunta por defecto a http://127.0.0.1:8000. Para generar la versión de producción, ejecutar `npm run build` desde `frontend`.

## Cálculo de comisiones

`Venta.calcular_comision()` ordena las reglas activas por monto mínimo de mayor a menor y aplica la primera cuyo mínimo sea menor o igual al monto de la venta. La comisión es `monto × porcentaje`. Si ninguna regla cumple, devuelve cero.

Una venta de $900 aplica la regla de 10% desde $800 y genera $90. Los reportes recalculan con las reglas actuales. Existe el modelo `ComisionCalculada`, pero el endpoint de cálculo no guarda automáticamente un historial en él.

**Datos heredados pendientes de revisión:** el fixture contiene 8% desde $500, 6% desde $600, 10% desde $800 y `1.1500` desde $1000. Este último valor representa **115%, no 15%**. Si el enunciado exige 15%, debe corregirse también en la base desplegada: editar el fixture no actualiza una base ya poblada.

## API principal

| Método | Ruta | Uso |
|---|---|---|
| GET / POST | `/api/vendedores/` | Listar / crear vendedores |
| GET / PUT / PATCH / DELETE | `/api/vendedores/{id}/` | Consultar / modificar / eliminar |
| GET | `/api/vendedores/{id}/ventas/` | Ventas del vendedor |
| GET | `/api/vendedores/{id}/comisiones/` | Resumen del vendedor |
| GET / POST | `/api/reglas/` | Listar reglas activas / crear |
| GET / PUT / PATCH / DELETE | `/api/reglas/{id}/` | Consultar / modificar / eliminar regla activa |
| GET / POST | `/api/ventas/` | Listar / crear ventas |
| GET / PUT / PATCH / DELETE | `/api/ventas/{id}/` | Consultar / modificar / eliminar |
| POST | `/api/comisiones/calcular/` | Reporte detallado por fechas |
| GET | `/api/comisiones/resumen/` | Resumen general con fechas opcionales |
| GET | `/api/comisiones-calculadas/` | Consultar registros de historial existentes |

La lista de ventas admite `vendedor`, `fecha_inicio` y `fecha_fin` como parámetros. El cálculo recibe:

```json
{"fecha_inicio": "2025-05-01", "fecha_fin": "2025-06-30"}
```

Se rechaza un rango cuya fecha de inicio sea posterior a la fecha de fin.

## Configuración de Render

Ambos servicios utilizan este repositorio y la rama `main`. La base PostgreSQL `mini-core-db` está en Oregon. Su Internal Database URL se configura como variable privada del backend.

### Backend: Web Service

| Campo | Valor |
|---|---|
| Name | `mini-core-backend` |
| Language | Python 3 |
| Region | Oregon |
| Root Directory | `backend` |
| Build Command | `bash build.sh` |
| Start Command | `python manage.py migrate && python manage.py seed_demo && gunicorn commission_project.wsgi:application --bind 0.0.0.0:$PORT` |

Variables del backend:

| KEY | VALUE |
|---|---|
| `PYTHON_VERSION` | `3.11.9` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Clave privada generada en Render |
| `DATABASE_URL` | Internal Database URL de PostgreSQL |
| `CORS_ALLOWED_ORIGINS` | `https://mini-core-frontend.onrender.com` |

`build.sh` instala dependencias y recopila estáticos. El inicio aplica migraciones, carga ejemplos si corresponde y arranca Gunicorn. Sin `DATABASE_URL`, Django utiliza SQLite.

### Frontend: Static Site

| Campo | Valor |
|---|---|
| Name | `mini-core-frontend` |
| Root Directory | `frontend` |
| Build Command | `npm ci && npm run build` |
| Publish Directory | `dist` |

Variables del frontend:

| KEY | VALUE |
|---|---|
| `VITE_API_URL` | `https://mini-core-backend-x00b.onrender.com` |

Las URLs se escriben sin `/` al final. `VITE_API_URL` no incluye `/api` porque Axios lo añade. Cambiar esta variable requiere recompilar el frontend; cambiar CORS requiere redesplegar el backend.

La base gratuita creada para esta entrega indica vencimiento el **12 de noviembre de 2026**. La disponibilidad de la demo depende de mantener activa la base.

## Alcance y créditos

Proyecto académico de demostración. La API permite operaciones sin autenticación: utilizar datos de prueba. Los logs de despliegue reportaron avisos de vulnerabilidades en dependencias npm; su revisión sigue pendiente.

- **Adaptación, ajustes visuales y despliegue:** Miguel Punin, UDLA.
- **Proyecto base de un semestre anterior:** [Mattair39/Proyecto-Mini-Core-MVC](https://github.com/Mattair39/Proyecto-Mini-Core-MVC).

Se conserva la atribución al proyecto base. Este repositorio no incluye un archivo `LICENSE`, por lo que esta documentación no declara una licencia MIT.
