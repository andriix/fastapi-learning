import datetime
from fastapi import APIRouter, HTTPException, status

from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep
from app.services.shipment import ShipmentService

router = APIRouter()

### Read a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    shipment = ShipmentService(session).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> Shipment:
    return await ShipmentService(session).add(shipment)


### Update fields of a shipment
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = await ShipmentService(session).update(shipment_update)
    
    return shipment


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    # Remove from database
    await ShipmentService(session).delete(id)

    return {"detail": f"Shipment with id #{id} is deleted!"}