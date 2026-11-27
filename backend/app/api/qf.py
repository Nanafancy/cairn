"""Read and simulation endpoints described in the project README.

The Soroban event indexer and database are not present in this repository yet,
so read endpoints return an empty collection until indexed data is available.
"""

from __future__ import annotations

from math import sqrt
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(tags=["rounds", "projects", "donors"])


class RoundList(BaseModel):
    items: list[dict[str, object]]
    total: int


class SimulationProject(BaseModel):
    project_id: str = Field(min_length=1)
    contributions: list[float] = Field(default_factory=list)


class SimulationRequest(BaseModel):
    projects: list[SimulationProject] = Field(min_length=1)
    matching_pool: float = Field(gt=0)
    per_donor_cap: float | None = Field(default=None, gt=0)
    allocation: Literal["quadratic"] = "quadratic"


class SimulationResult(BaseModel):
    project_id: str
    total_donated: float
    donor_count: int
    raw_match: float
    match: float


@router.get("/rounds", response_model=RoundList)
def list_rounds(
    status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> RoundList:
    """List indexed rounds. The indexer is not configured in this starter."""
    del status, limit, offset
    return RoundList(items=[], total=0)


@router.get("/rounds/{round_id}")
def get_round(round_id: str) -> dict[str, object]:
    raise HTTPException(status_code=404, detail=f"Round '{round_id}' was not found")


@router.get("/rounds/{round_id}/projects")
def list_round_projects(round_id: str) -> dict[str, object]:
    raise HTTPException(status_code=404, detail=f"Round '{round_id}' was not found")


@router.get("/projects/{project_id}")
def get_project(project_id: str) -> dict[str, object]:
    raise HTTPException(status_code=404, detail=f"Project '{project_id}' was not found")


@router.post("/rounds/{round_id}/simulate", response_model=list[SimulationResult])
def simulate_round(round_id: str, request: SimulationRequest) -> list[SimulationResult]:
    """Estimate quadratic matches for supplied hypothetical contributions.

    Contributions use the same token units as ``matching_pool``. A donor's
    cumulative contributions to a project are capped before applying QF.
    The available pool is allocated proportionally to each project's raw
    quadratic match, and rounds without any match return zero allocations.
    """
    del round_id  # Simulation is independent of indexed round state.
    if len({project.project_id for project in request.projects}) != len(request.projects):
        raise HTTPException(status_code=422, detail="project_id values must be unique")

    raw_matches: list[float] = []
    totals: list[tuple[float, int]] = []
    for project in request.projects:
        if any(amount < 0 for amount in project.contributions):
            raise HTTPException(status_code=422, detail="contributions must be non-negative")
        contributions = [
            min(amount, request.per_donor_cap)
            if request.per_donor_cap is not None
            else amount
            for amount in project.contributions
        ]
        total = sum(contributions)
        root_sum = sum(sqrt(amount) for amount in contributions)
        raw_matches.append(max(0.0, root_sum * root_sum - total))
        totals.append((total, sum(amount > 0 for amount in contributions)))

    raw_total = sum(raw_matches)
    return [
        SimulationResult(
            project_id=project.project_id,
            total_donated=totals[index][0],
            donor_count=totals[index][1],
            raw_match=raw_matches[index],
            match=(request.matching_pool * raw_matches[index] / raw_total if raw_total else 0.0),
        )
        for index, project in enumerate(request.projects)
    ]


@router.get("/donors/{address}/history")
def donor_history(address: str) -> dict[str, object]:
    """Return indexed donations for a wallet (empty until the indexer exists)."""
    return {"address": address, "items": [], "total": 0}
