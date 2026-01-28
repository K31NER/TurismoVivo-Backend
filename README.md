# Turismo Vivo Backend

Backend para la plataforma **Turismo Vivo**, construido con **FastAPI** implementando una arquitectura basada en **Domain-Driven Design (DDD)** y **Clean Architecture**.

## 🏗 Arquitectura del Proyecto

El proyecto sigue una estricta separación de responsabilidades, asegurando que la lógica de negocio (Dominio) sea el núcleo independiente de frameworks y bases de datos.

###  Capas del Sistema (De adentro hacia afuera)

1.  **Domain (`src/domain/`)** 
    *   **Responsabilidad:** Contiene la lógica de negocio pura y las reglas empresariales.
    *   **Contenido:** Entidades (`Service`), Enums (`ServiceStatus`) y Excepciones.
    *   **Regla de Oro:** No depende de **nada** externo (ni FastAPI, ni DB). Solo Python puro.

2.  **Repository Interface (`src/repository/`)** 
    *   **Responsabilidad:** Define el **contrato** para acceder a los datos.
    *   **Contenido:** Clases abstractas (`ABC`) que dictan qué métodos existen (`create`, `get_by_id`).
    *   **Objetivo:** Permitir cambiar la base de datos sin tocar la lógica de negocio.

3.  **Use Case (`src/use_case/`)** 
    *   **Responsabilidad:** Orquesta los flujos de la aplicación.
    *   **Acción:** Recibe datos, ejecuta validaciones del Dominio y llama al Repositorio.
    *   **Ejemplo:** `UseServices` maneja la creación de servicios, validando precios y fechas antes de guardar.

4.  **Infrastructure (`src/infrastructure/`)** 
    *   **Responsabilidad:** Implementación técnica concreta ("El mundo real").
    *   **Contenido:** Adaptadores de Base de Datos (`SupabaseServiceRepository`), Modelos de BD, Clientes externos.
    *   **Detalle:** Aquí es donde se usa la librería de `supabase`.

5.  **API (`src/api/`)** 
    *   **Responsabilidad:** Capa de presentación (HTTP).
    *   **Contenido:** Routers (Endpoints) y Schemas (DTOs de entrada/salida).
    *   **Detalle:** Maneja la conversión de JSON a objetos y códigos de estado HTTP status (200, 404, 500).

## 📂 Estructura de Carpetas

```text
src/
├── api/                # Capa de Presentación (Routers y Schemas)
│   ├── routers/        # Endpoints de FastAPI
│   └── schemas/        # Pydantic Models (DTOs)
├── config/             # Configuración (Variables de entorno, Clientes)
├── domain/             # Lógica de Negocio (Entidades Puras)
├── infrastructure/     # Implementación Técnica (Base de Datos, APIs)
├── repository/         # Interfaces y Contratos de Datos
├── use_case/           # Lógica de Aplicación (Servicios)
└── main.py             # Punto de entrada
```

## Tecnologías

*   **Lenguaje:** Python 3.11+
*   **Framework Web:** FastAPI
*   **Base de Datos:** PostgreSQL (vía Supabase)
*   **Validación de Datos:** Pydantic
*   **Gestor de Paquetes:** Pip / Venv
