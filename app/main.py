from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response

from . import db

from .models import CarInput


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Prepare the database before the application accepts requests."""
    db.initialize()

    # Startup is complete. FastAPI serves requests while execution is paused here.
    yield

    # Shutdown cleanup would go below yield if we needed it.
    # Our database helpers already close their own connections.


app = FastAPI(
    title="Car Catalogue API",
    lifespan=lifespan,
)


@app.get("/api/health")
def health():
    """Confirm that the application can respond."""
    return {"status": "ok"}


@app.get("/api/cars")
def list_cars(q: str = "", category: str | None = None):
    """Read matching cars from the application database."""
    return db.list_cars(q=q, category=category)


@app.get("/api/cars/{car_id}")
def get_car(car_id: int):
    """Read one car and translate a missing record into HTTP 404."""
    car = db.get_car(car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="This car does not exist.",
        )

    return car

# Connect validated HTTP requests to database writes.
@app.post("/api/cars", status_code=201)
def create_car(data: CarInput):
    """Validate the request, create a car, and return its stored content."""
    # Pass plain data to the database layer.
    return db.create_car(data.model_dump())


@app.put("/api/cars/{car_id}")
def update_car(car_id: int, data: CarInput):
    """Replace an existing car's editable content."""
    car = db.update_car(car_id, data.model_dump())

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="This car does not exist.",
        )

    return car


@app.delete("/api/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    """Delete a car and return an empty success response."""
    deleted = db.delete_car(car_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="This car does not exist.",
        )

    return Response(status_code=204)