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
                 │
┌────────────────▼────────────────────────────────────┐
│                  Service Layer                      │
│              (Business logic)                       │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│                Repository Layer                     │
│           (Data access / CRUD)                      │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────┐
│                   Model Layer                       │
│          (Schema & validation)                      │
└─────────────────────────────────────────────────────┘
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
- Returns formatted JSON responses

### 5. **Routes Layer** (`routes/`)
- Clean API endpoint definitions
- Maps URLs to controller methods
- Similar to NestJS route decorators

## API Endpoints

All endpoints are prefixed with `/api` (global prefix):

```
GET  /health                              - Health check
GET  /api/wells                          - Get all wells
GET  /api/wells/summary                  - Get wells summary
GET  /api/wells/:name                    - Get specific well
GET  /api/wells/:name/exists             - Check if well exists
GET  /api/wells/search/inline            - Search by inline range
     ?min=X&max=Y
GET  /api/wells/search/crossline         - Search by crossline range
     ?min=X&max=Y
GET  /api/wells/search/area              - Search by area
     ?min_inline=X&max_inline=Y
     &min_crossline=A&max_crossline=B
```

## Running the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if needed)
pip install flask flask-cors

# Run the server
python main.py
```

The server will start on `http://localhost:5000`

## Testing Endpoints

```bash
# Health check
curl http://localhost:5000/health

# Get all wells
curl http://localhost:5000/api/wells

# Get wells summary
curl http://localhost:5000/api/wells/summary

# Get specific well
curl http://localhost:5000/api/wells/100

# Search by inline range
curl "http://localhost:5000/api/wells/search/inline?min=10000&max=10600"

# Search by area
curl "http://localhost:5000/api/wells/search/area?min_inline=10000&max_inline=10600&min_crossline=1200&max_crossline=1300"
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
