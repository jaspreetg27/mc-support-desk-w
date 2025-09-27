"""Customer router with read-only operations."""

import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Customer
from ..deps import get_db
from ..logging import get_logger
from ..schemas.common import PaginatedResponse, PaginationParams
from ..schemas.customer import CustomerResponse

router = APIRouter(prefix="/customers", tags=["customers"])
logger = get_logger(__name__)


@router.get("", response_model=PaginatedResponse)
async def list_customers(
    tenant_id: Optional[uuid.UUID] = Query(None, description="Filter by tenant ID"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse:
    """List customers with optional filtering by tenant and platform."""
    
    # Build base query
    base_stmt = select(Customer)
    count_stmt = select(func.count(Customer.id))
    
    # Apply filters
    if tenant_id:
        base_stmt = base_stmt.where(Customer.tenant_id == tenant_id)
        count_stmt = count_stmt.where(Customer.tenant_id == tenant_id)
    
    if platform:
        base_stmt = base_stmt.where(Customer.platform == platform)
        count_stmt = count_stmt.where(Customer.platform == platform)
    
    # Get total count
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Get paginated results
    stmt = (
        base_stmt
        .order_by(Customer.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    customers = result.scalars().all()
    
    customer_responses = [CustomerResponse.model_validate(customer) for customer in customers]
    
    logger.info(
        "Listed customers",
        total=total,
        returned=len(customer_responses),
        tenant_id=str(tenant_id) if tenant_id else None,
        platform=platform,
        skip=pagination.skip,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=customer_responses,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit,
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CustomerResponse:
    """Get a specific customer by ID."""
    
    stmt = select(Customer).where(Customer.id == customer_id)
    result = await db.execute(stmt)
    customer = result.scalar_one_or_none()
    
    if not customer:
        logger.warning("Customer not found", customer_id=str(customer_id))
        raise HTTPException(status_code=404, detail="Customer not found")
    
    logger.info(
        "Retrieved customer",
        customer_id=str(customer_id),
        platform=customer.platform,
        platform_user_id=customer.platform_user_id,
    )
    
    return CustomerResponse.model_validate(customer)
