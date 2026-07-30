# Smart Building Sensor Service

Practice project demonstrating

- FastAPI
- Clean Architecture
- Repository Pattern
- Event Driven Design
- Unit Testing
- Docker

## Run

```bash
uvicorn app.main:app --reload
```

Open

http://localhost:8000/docs


FastAPI
                   │
              API Routers
                   │
            SensorService
             │         │
             │         │
      Repository    Publisher