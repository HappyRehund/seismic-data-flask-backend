# Flask Seismic Viewer Backend

## Architecture Overview

This backend follows clean architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                    Routes Layer                     │
│          (API endpoint definitions)                 │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│                 Controller Layer                    │
│         (HTTP request/response handling)            │
└────────────────┬────────────────────────────────────┘
                 │           uses ───────────────────────┐
┌────────────────▼────────────────────────────────────┐  │
│                  Service Layer                      │  │
│              (Business logic)                       │  │
└────────────────┬────────────────────────────────────┘  │
                 │                                       │
┌────────────────▼────────────────────────────────────┐  │
│                Repository Layer                     │  │
│           (Data access / CRUD)                      │  │
└────────────────┬────────────────────────────────────┘  │
                 │                                       │
┌────────────────▼────────────────────────────────────┐  │
│                   Model Layer                       │  │
│          (Schema & validation)                      │  │
└─────────────────────────────────────────────────────┘  │
                                                         │
┌────────────────────────────────────────────────────────▼┐
│                    Shared Utilities                     │
│  ┌──────────────────────┐  ┌──────────────────────┐     │
│  │    dto/              │  │    common/            │    │
│  │  (Data Transfer      │  │  (Shared helpers &    │    │
│  │   Objects)           │  │   response utils)     │    │
│  └──────────────────────┘  └──────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Folder Structure

```
backend/
├── main.py                     # App factory & entry point
├── pyproject.toml              # Project metadata & dependencies (uv)
├── models/                     # Data schemas & validation
├── repositories/               # Data access layer (CSV / DB)
├── services/                   # Business logic
├── controllers/                # HTTP request/response handling
├── routes/                     # API route definitions
├── dto/                        # Data Transfer Objects
└── common/                     # Shared cross-cutting utilities
    ├── response_utils.py       # success_response, error_response, file_response
    └── well_name_utils.py      # normalize_well_name helper
```

## Layer Responsibilities

### 1. **Model Layer** (`models/`)
- Defines data schemas with validation
- Similar to Mongoose schemas in NestJS
- Example: `WellCoordinate` dataclass with type validation

### 2. **Repository Layer** (`repositories/`)
- Handles all data access operations (CRUD)
- Centralizes database/CSV interactions
- Similar to TypeORM repositories
- Currently using CSV, easily replaceable with SQL/NoSQL

### 3. **Service Layer** (`services/`)
- Contains business logic
- Orchestrates operations across repositories
- Validates business rules
- Transforms data for presentation

### 4. **Controller Layer** (`controllers/`)
- Handles HTTP requests/responses
- Validates input parameters
- Calls appropriate service methods
- Returns formatted JSON responses via `common/response_utils.py`

### 5. **Routes Layer** (`routes/`)
- Clean API endpoint definitions
- Maps URLs to controller methods
- Similar to NestJS route decorators

### 6. **DTO Layer** (`dto/`)
- Defines typed contracts for data flowing in and out of the API
- `dto/base.py` — `DtoResponse` protocol and `ListResponse` generic wrapper
- `dto/data/` — Inbound DTOs for parsing raw CSV/DB data into typed objects
- `dto/response/` — Outbound response DTOs serialized to JSON

### 7. **Common Utilities** (`common/`)
- Shared helpers used across layers (not business logic)
- `response_utils.py` — Standardized `success_response`, `error_response`, and `file_response` builders
- `well_name_utils.py` — `normalize_well_name` for consistent well name formatting (e.g. `GNK-001`)

## API Endpoints

All endpoints are prefixed with `/api` (global prefix):

```
GET  /health                                      - Health check

# Wells
GET  /api/well                                    - Get all wells
GET  /api/well/summary                            - Get wells summary
GET  /api/well/:well_name                         - Get specific well by name
GET  /api/well/:well_name/exists                  - Check if well exists

# Well Logs
GET  /api/well-log                                - Get all well logs
     ?page=1&page_size=500
GET  /api/well-log/:well_name                     - Get well logs by well name

# Horizons
GET  /api/horizon                                 - Get all horizons
     ?page=1&page_size=500

# Seismic Sections (returns PNG image)
GET  /api/inline/:number/image                    - Get inline section image
GET  /api/crossline/:number/image                 - Get crossline section image
```

### Response Format

All JSON endpoints return a standardized envelope:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message"
}
```

**List responses** include a `count` field inside `data`:
```json
{
  "success": true,
  "data": {
    "wells": [ ... ],
    "count": 42
  }
}
```

**Seismic section endpoints** return a raw `image/png` binary response (not JSON).

## Setup & Running the Application

This project uses [uv](https://docs.astral.sh/uv/) as the package manager.

### Prerequisites

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installation

```bash
# Clone / navigate to the project
cd backend

# Create virtual environment and install all dependencies
uv sync
```

### Running the Server

```bash
# Run directly via uv (no manual activation needed)
uv run python main.py

# Or activate the virtual environment first, then run
source .venv/bin/activate
python main.py
```

The server will start on `http://localhost:5000`

### Adding Dependencies

```bash
# Add a new package
uv add <package-name>

# Add a dev-only package
uv add --dev <package-name>
```

## Testing Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Get all wells
curl http://localhost:5000/api/well

# Get wells summary
curl http://localhost:5000/api/well/summary

# Get specific well
curl http://localhost:5000/api/well/GNK-001

# Check if well exists
curl http://localhost:5000/api/well/GNK-001/exists

# Get all well logs (with pagination)
curl "http://localhost:5000/api/well-log?page=1&page_size=100"

# Get well logs for a specific well
curl http://localhost:5000/api/well-log/GNK-001

# Get all horizons (with pagination)
curl "http://localhost:5000/api/horizon?page=1&page_size=500"

# Get inline seismic section image
curl http://localhost:5000/api/inline/100/image --output inline_100.png

# Get crossline seismic section image
curl http://localhost:5000/api/crossline/200/image --output crossline_200.png
```

## Migration Path to Real Database

When ready to move from CSV to a real database:

1. **Keep the same architecture** - only modify the Repository layer
2. **Update Repository** to use SQLAlchemy, MongoDB, etc.
3. **Services, Controllers, Routes remain unchanged**
4. **Models** can be enhanced with ORM decorators

Example future repository:
```python
class WellRepository:
    def find_all(self):
        return db.session.query(WellCoordinate).all()
```

## Benefits of This Architecture

✅ **Separation of Concerns** - Each layer has a single responsibility
✅ **Testability** - Easy to unit test each layer independently
✅ **Maintainability** - Changes in one layer don't affect others
✅ **Scalability** - Easy to add new features/endpoints
✅ **Database Agnostic** - Easy to swap data sources
✅ **Familiar** - Similar to NestJS/TypeScript patterns
✅ **Typed Contracts** - DTOs enforce clear data shapes across layer boundaries
✅ **DRY Utilities** - Shared `common/` helpers prevent duplicated response logic
