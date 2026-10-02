from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime, timezone

app = FastAPI(title="ClaimMate Digital Claims & Authority Bridge")

# ================================================================
# CAPABILITY 1: DIGIO VERIFIABLE POWER-OF-ATTORNEY (AUTHORITY RAIL)
# ================================================================

class PoARequest(BaseModel):
    claimant_name: str
    policy_number: str
    tpa_name: str
    scope: str = "INSURANCE_CLAIM_ADJUDICATION"

@app.post("/api/v2/authority/poa_generate")
async def generate_poa(req: PoARequest):
    poa_id = f"did:digio:poa:{uuid.uuid4().hex[:12]}"
    return {
        "status": "ISSUED",
        "poa_token": poa_id,
        "claimant": req.claimant_name,
        "authorized_representative": "ClaimMate AI (Autonomous Legal Proxy)",
        "counterparty": req.tpa_name,
        "scope": req.scope,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "valid_until": "2026-10-31T23:59:59Z",
        "verification_uri": f"https://mock.digio.in/v/{poa_id}"
    }


# ================================================================
# CAPABILITY 2: DIGITAL HEALTH DATA & E-BILL RETRIEVAL
# ================================================================

@app.get("/api/v1/health_data/fetch_certified_bills")
async def fetch_certified_bills(policy_number: str, consent_token: str):

    if consent_token == "EXPIRED":
        return {
            "success": False,
            "error": "CONSENT_EXPIRED",
            "message": "User consent handle has expired. Prompt user for re-authentication."
        }

    return {
        "success": True,
        "hospital_name": "Apollo Hospitals, Bangalore",
        "hospital_reg_no": "KA-BLR-HOSP-2021",
        "patient_name": "Ramesh Kumar",
        "total_amount_inr": 78500,
        "digital_stamp_verified": True,
        "doctor_registration_no": "KMC-48291",
        "icd_10_codes": ["E03.9", "Z01.812"],
        "documents": [
            {
                "type": "DISCHARGE_SUMMARY",
                "url": "https://storage.mock/docs/discharge_summary_certified.pdf",
                "verified": True
            },
            {
                "type": "FINAL_ITEMIZED_BILL",
                "url": "https://storage.mock/docs/itemized_bill_signed.pdf",
                "verified": True
            }
        ]
    }


# ================================================================
# CAPABILITY 3: TPA CLAIMS & GRIEVANCE ESCALATION PORTAL
# ================================================================

class AppealSubmission(BaseModel):
    policy_number: str
    denial_code: str
    appeal_summary: str
    evidence_urls: List[str]
    escalation_level: str = "TPA_INTERNAL"


@app.post("/api/v1/tpa/submit_appeal")
async def submit_tpa_appeal(appeal: AppealSubmission):

    # Failure simulation for evaluation testing
    if appeal.denial_code == "TIMEOUT_TEST":
        raise HTTPException(
            status_code=504,
            detail="TPA Grievance Portal Gateway Timeout"
        )

    appeal_id = f"APL-{uuid.uuid4().hex[:8].upper()}"

    return {
        "success": True,
        "appeal_id": appeal_id,
        "status": "UNDER_REVIEW",
        "escalation_level": appeal.escalation_level,
        "turnaround_time_hours": 48,
        "submission_timestamp": datetime.now(timezone.utc).isoformat(),
        "acknowledgement": (
            f"Appeal for denial {appeal.denial_code} "
            f"formally logged under reference {appeal_id}."
        )
    }


# ================================================================
# PINE LABS DISPUTE & CHARGEBACK EXTENSION
# ================================================================

class DisputeLockRequest(BaseModel):
    order_id: str
    amount_paise: int
    dispute_reason: str


@app.post("/api/v1/pinelabs_ext/chargeback_lock")
async def create_chargeback_lock(req: DisputeLockRequest):

    return {
        "status": "DISPUTE_RAISED",
        "dispute_ref": f"PL-DISP-{uuid.uuid4().hex[:6].upper()}",
        "order_id": req.order_id,
        "amount_inr": req.amount_paise / 100,
        "reason": req.dispute_reason,
        "mandate_frozen": True
    }
