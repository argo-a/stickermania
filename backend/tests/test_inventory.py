import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.trading import CompanyInventory, InventoryMovement, MovementType

def test_create_company_inventory(db_session):
    """Test creating a company inventory item"""
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100,
        company_inventory_quantity_allocated=0,
        is_active=True,
        restock_threshold=20,
        notes="Test inventory",
        meta_info={"supplier": "Panini"}
    )
    db_session.add(inventory)
    db_session.commit()

    assert inventory.id is not None
    assert inventory.company_inventory_item_type == "pack"
    assert inventory.company_inventory_quantity_available == 100
    assert inventory.is_active is True
    assert inventory.meta_info["supplier"] == "Panini"

def test_create_company_inventory_required_fields(db_session):
    """Test creating a company inventory with only required fields"""
    inventory = CompanyInventory(
        company_inventory_item_type="card",
        company_inventory_item_id=1,
        company_inventory_quantity_available=50
    )
    db_session.add(inventory)
    db_session.commit()

    assert inventory.id is not None
    assert inventory.company_inventory_item_type == "card"
    assert inventory.company_inventory_quantity_available == 50
    assert inventory.notes is None
    assert inventory.meta_info is None

def test_create_company_inventory_missing_required(db_session):
    """Test creating a company inventory without required fields fails"""
    inventory = CompanyInventory(
        company_inventory_quantity_available=100  # Missing item_type and item_id
    )
    with pytest.raises(IntegrityError):
        db_session.add(inventory)
        db_session.commit()

def test_create_inventory_movement(db_session):
    """Test creating an inventory movement"""
    # First create an inventory item
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100
    )
    db_session.add(inventory)
    db_session.commit()

    # Create a movement
    movement = InventoryMovement(
        inventory_id=inventory.id,
        inventory_movement_type=MovementType.RESTOCK.value,
        inventory_movement_quantity=50,
        notes="Initial stock",
        meta_info={"purchase_order": "PO123"}
    )
    db_session.add(movement)
    db_session.commit()

    assert movement.id is not None
    assert movement.inventory_movement_type == MovementType.RESTOCK.value
    assert movement.inventory_movement_quantity == 50
    assert isinstance(movement.inventory_movement_created_at, datetime)
    assert movement.meta_info["purchase_order"] == "PO123"

def test_create_inventory_movement_required_fields(db_session):
    """Test creating an inventory movement with only required fields"""
    # First create an inventory item
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100
    )
    db_session.add(inventory)
    db_session.commit()

    # Create a movement with only required fields
    movement = InventoryMovement(
        inventory_id=inventory.id,
        inventory_movement_type=MovementType.SALE.value,
        inventory_movement_quantity=25
    )
    db_session.add(movement)
    db_session.commit()

    assert movement.id is not None
    assert movement.inventory_movement_type == MovementType.SALE.value
    assert movement.notes is None
    assert movement.meta_info is None

def test_create_inventory_movement_missing_required(db_session):
    """Test creating an inventory movement without required fields fails"""
    movement = InventoryMovement(
        inventory_movement_quantity=50  # Missing inventory_id and movement_type
    )
    with pytest.raises(IntegrityError):
        db_session.add(movement)
        db_session.commit()

def test_inventory_movement_relationship(db_session):
    """Test relationship between inventory and movements"""
    # Create inventory item
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100
    )
    db_session.add(inventory)
    db_session.commit()

    # Create multiple movements
    movement1 = InventoryMovement(
        inventory_id=inventory.id,
        inventory_movement_type=MovementType.RESTOCK.value,
        inventory_movement_quantity=50
    )
    movement2 = InventoryMovement(
        inventory_id=inventory.id,
        inventory_movement_type=MovementType.SALE.value,
        inventory_movement_quantity=20
    )
    db_session.add_all([movement1, movement2])
    db_session.commit()

    # Test relationships
    assert len(inventory.movements) == 2
    assert movement1.inventory_item == inventory
    assert movement2.inventory_item == inventory

def test_inventory_movement_types(db_session):
    """Test all inventory movement types"""
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100
    )
    db_session.add(inventory)
    db_session.commit()

    # Test each movement type
    movement_types = [
        MovementType.RESTOCK.value,
        MovementType.SALE.value,
        MovementType.RETURN.value,
        MovementType.ADJUSTMENT.value,
        MovementType.TRADE.value
    ]

    for movement_type in movement_types:
        movement = InventoryMovement(
            inventory_id=inventory.id,
            inventory_movement_type=movement_type,
            inventory_movement_quantity=10
        )
        db_session.add(movement)
        db_session.commit()

        assert movement.id is not None
        assert movement.inventory_movement_type == movement_type

def test_inventory_meta_info(db_session):
    """Test inventory meta_info"""
    inventory = CompanyInventory(
        company_inventory_item_type="pack",
        company_inventory_item_id=1,
        company_inventory_quantity_available=100,
        meta_info={
            "supplier": "Panini",
            "batch_info": {
                "production_date": "2023-01-01",
                "quality_check": "passed"
            }
        }
    )
    db_session.add(inventory)
    db_session.commit()

    assert inventory.meta_info["supplier"] == "Panini"
    assert inventory.meta_info["batch_info"]["quality_check"] == "passed"
