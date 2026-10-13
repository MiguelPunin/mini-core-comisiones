# Mini Core: Sistema de ventas y comisiones

Proyecto para la **Tarea 4: Aplicación Ejercicio MVC** de la Universidad de las Américas (UDLA), desarrollado a partir del ejercicio de un semestre anterior.

**Estudiante:** Miguel Punin ([MiguelPunin](https://github.com/MiguelPunin)).
**Asignatura:** Desarrollo Web, semestre 7.

Sistema de registro de ventas y cálculo de comisiones. Permite consultar cuánto vendió cada vendedor y qué comisión le corresponde en un período determinado. El frontend está hecho con React y el backend con Django REST Framework; ambos están desplegados en Render con una base de datos PostgreSQL.

## Aplicación desplegada

| Recurso | Enlace |
|---|---|
| Frontend | [Abrir aplicación](https://mini-core-frontend.onrender.com) |
| Backend | [Abrir API](https://mini-core-backend-x00b.onrender.com/api/) |
| Repositorio | [mini-core-comisiones](https://github.com/MiguelPunin/mini-core-comisiones) |

Para usar el sistema, abre el enlace del frontend. El enlace del backend permite consultar los endpoints de la API.

## Video de presentación

[Ver la explicación del proyecto y su despliegue en Render](https://youtu.be/pOxcq_3OZtQ).

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

El proyecto separa los datos, el manejo de peticiones y la presentación. En Django, `models.py` define las tablas y el cálculo de comisiones, mientras que `views.py` recibe las peticiones y devuelve JSON. React consume esas respuestas y muestra la interfaz. Django utiliza la organización MVT; en este proyecto, la presentación de la aplicación se resuelve con React.

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

Necesitas Python 3.11 y Node.js con npm. Ejecuta el backend y el frontend en terminales separadas.

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

Estos comandos crean el entorno `.venv` en la raíz y utilizan su ejecutable directamente, sin necesidad de activarlo. La API queda disponible en http://127.0.0.1:8000/api/.

`seed_demo` carga cuatro vendedores, cuatro reglas y cinco ventas únicamente si las tablas de vendedores, reglas y ventas están vacías. Las ventas de ejemplo son de mayo y junio de 2025: seleccionar ese período para verlas en los reportes.

### Frontend

En otra terminal, desde la raíz del proyecto:

```powershell
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Abre http://127.0.0.1:3000/. El frontend se conecta por defecto al backend en http://127.0.0.1:8000.

Para compilar la aplicación, ejecuta desde `frontend`:

```powershell
npm run build
```

### Prueba rápida

1. Selecciona un vendedor y registra una venta de $900.
2. Comprueba que la tabla muestre una comisión de $90 (10%).
3. Abre la pestaña de comisiones y elige un rango que incluya la fecha de la venta.
4. Calcula el reporte y despliega el detalle del vendedor.

## Cálculo de comisiones

`Venta.calcular_comision()` ordena las reglas activas por monto mínimo de mayor a menor y aplica la primera cuyo mínimo sea menor o igual al monto de la venta. La comisión es `monto × porcentaje`. Si ninguna regla cumple, devuelve cero.

Una venta de $900 aplica la regla de 10% desde $800 y genera $90. Los reportes recalculan con las reglas actuales. Existe el modelo `ComisionCalculada`, pero el endpoint de cálculo no guarda automáticamente un historial en él.

**Nota sobre los ejemplos:** el archivo inicial contiene una regla con porcentaje `1.1500`, equivalente a 115%. Para representar 15%, el valor debe ser `0.1500`. Si la base ya tiene datos, cambiar el archivo no actualiza esa regla automáticamente.

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

## Créditos

- **Adaptación, ajustes visuales y despliegue:** Miguel Punin, UDLA.
- **Proyecto base de un semestre anterior:** [Mattair39/Proyecto-Mini-Core-MVC](https://github.com/Mattair39/Proyecto-Mini-Core-MVC).
