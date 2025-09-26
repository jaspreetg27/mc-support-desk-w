"""Tenant router with read-only operations."""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models import Tenant
from ..deps import get_db
from ..logging import get_logger
from ..schemas.common import PaginatedResponse, PaginationParams
from ..schemas.tenant import TenantResponse

router = APIRouter(prefix="/tenants", tags=["tenants"])
logger = get_logger(__name__)


@router.get("", response_model=PaginatedResponse)
async def list_tenants(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse:
    """List all tenants with pagination."""
    
    # Get total count
    count_stmt = select(func.count(Tenant.id))
    total_result = await db.execute(count_stmt)
    total = total_result.scalar() or 0
    
    # Get paginated results
    stmt = (
        select(Tenant)
        .order_by(Tenant.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    result = await db.execute(stmt)
    tenants = result.scalars().all()
    
    tenant_responses = [TenantResponse.model_validate(tenant) for tenant in tenants]
    
    logger.info(
        "Listed tenants",
        total=total,
        returned=len(tenant_responses),
        skip=pagination.skip,
        limit=pagination.limit,
    )
    
    return PaginatedResponse.create(
        items=tenant_responses,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit,
    )


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> TenantResponse:
    """Get a specific tenant by ID."""
    
    stmt = select(Tenant).where(Tenant.id == tenant_id)
    result = await db.execute(stmt)
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        logger.warning("Tenant not found", tenant_id=str(tenant_id))
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    logger.info("Retrieved tenant", tenant_id=str(tenant_id), tenant_name=tenant.name)
    
    return TenantResponse.model_validate(tenant)
