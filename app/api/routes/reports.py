from typing import Any

import requests

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.dependencies import get_current_user
from app.services.supabase_service import (
    SUPABASE_URL,
    get_supabase_headers,
)


router = APIRouter(
    prefix="/reports",
    tags=["Research Reports"],
)


class ResearchReportRequest(BaseModel):
    ticker: str = Field(min_length=1, max_length=20)
    company_name: str | None = None
    report_data: dict[str, Any]


def get_reports_url() -> str:
    if not SUPABASE_URL:
        raise HTTPException(
            status_code=503,
            detail="Supabase is not configured.",
        )

    return f"{SUPABASE_URL.rstrip('/')}/rest/v1/research_reports"


def handle_supabase_error(error: requests.RequestException):
    raise HTTPException(
        status_code=502,
        detail="Unable to complete the research report operation.",
    ) from error


@router.post("", status_code=status.HTTP_201_CREATED)
def save_report(
    report: ResearchReportRequest,
    user: dict = Depends(get_current_user),
):
    headers = get_supabase_headers(user["access_token"])

    headers["Prefer"] = "return=representation"

    payload = {
        "user_id": user["id"],
        "ticker": report.ticker.strip().upper(),
        "company_name": report.company_name,
        "report_data": report.report_data,
    }

    try:
        response = requests.post(
            get_reports_url(),
            headers=headers,
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        handle_supabase_error(error)


@router.get("")
def list_reports(
    user: dict = Depends(get_current_user),
):
    headers = get_supabase_headers(user["access_token"])

    params = {
        "select": "id,ticker,company_name,created_at,updated_at",
        "user_id": f"eq.{user['id']}",
        "order": "created_at.desc",
    }

    try:
        response = requests.get(
            get_reports_url(),
            headers=headers,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        handle_supabase_error(error)


@router.get("/{report_id}")
def get_report(
    report_id: str,
    user: dict = Depends(get_current_user),
):
    headers = get_supabase_headers(user["access_token"])

    params = {
        "select": "*",
        "id": f"eq.{report_id}",
        "user_id": f"eq.{user['id']}",
    }

    try:
        response = requests.get(
            get_reports_url(),
            headers=headers,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        reports = response.json()

        if not reports:
            raise HTTPException(
                status_code=404,
                detail="Research report not found.",
            )

        return reports[0]

    except requests.RequestException as error:
        handle_supabase_error(error)


@router.delete("/{report_id}")
def delete_report(
    report_id: str,
    user: dict = Depends(get_current_user),
):
    headers = get_supabase_headers(user["access_token"])

    params = {
        "id": f"eq.{report_id}",
        "user_id": f"eq.{user['id']}",
    }

    try:
        response = requests.delete(
            get_reports_url(),
            headers=headers,
            params=params,
            timeout=20,
        )
        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            return {"message": "Research report deleted successfully."}

        return response.json()

    except requests.RequestException as error:
        handle_supabase_error(error)
