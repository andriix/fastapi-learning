import datetime
from fastapi import APIRouter, HTTPException, status

from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database.models import Shipment, ShipmentStatus
from app.database.session import SessionDep

router = APIRouter()

### Read a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session: SessionDep):
    # Check for shipment with given id
    shipment = await session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@router.post("/shipment", response_model=None)
async def submit_shipment(shipment: ShipmentCreate, session: SessionDep) -> dict[str, int]:
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + datetime.timedelta(days=3),
    )
    session.add(new_shipment)
    await session.commit()
    await session.refresh(new_shipment)

    return {"id": new_shipment.id}


### Update fields of a shipment
@router.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, shipment_update: ShipmentUpdate, session: SessionDep):
    # Update data with given fields
    update = shipment_update.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update",
        )

    shipment = session.get(Shipment, id)
    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


### Delete a shipment by id
@router.delete("/shipment")
def delete_shipment(id: int, session: SessionDep) -> dict[str, str]:
    # Remove from database
    session.delete(session.get(Shipment, id))
    session.commit()

    return {"detail": f"Shipment with id #{id} is deleted!"}