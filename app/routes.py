"""Define the API endpoints and trasnlate datatabase results into HTTP Responses"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, Query

from . import db

from .models import CarInput, Car, Category

# A router is a group of related endpoints
# Every route starts with /api
# and appears under the "Catalogue" Title in fastapi DOCS
# APIRouter is the fastapi tool that creates the group (the object). Router is just the name of the variable holding it
router = APIRouter(prefix="/api", tags=["Catalogue"])

@router.get("/health")
def health():
    """Confirm that the application can respond."""
    return {"status": "ok"}


# @router.get("/cars", response_model=list[Car])
# def list_cars(q: str = "", category: str | None = None):
#     """Read matching cars from the application database."""
#     return db.list_cars(q=q, category=category)

@router.get("/cars", response_model=list[Car])
def list_cars(q: Annotated[str, Query(max_length=100, description="Search the name, manufacturer, or description",),] = "", category: Category | None = None):
    """Read matching cars from the application database."""
    return db.list_cars(q=q, category=category)

@router.get("/cars/{car_id}", response_model=Car)
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
@router.post("/cars", status_code=201, response_model=Car)
def create_car(data: CarInput):
    """Validate the request, create a car, and return its stored content."""
    # Pass plain data to the database layer.
    return db.create_car(data.model_dump())


@router.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: int, data: CarInput):
    """Replace an existing car's editable content."""
    car = db.update_car(car_id, data.model_dump())

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="This car does not exist.",
        )

    return car


@router.delete("/cars/{car_id}", status_code=204)
def delete_car(car_id: int):
    """Delete a car and return an empty success response."""
    deleted = db.delete_car(car_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="This car does not exist.",
        )

    return Response(status_code=204)

