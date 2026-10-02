from mcp.server.mcpserver import MCPServer
from mcp.server.transport_security import TransportSecuritySettings
from typing import List
import uuid
from datetime import datetime, timezone

mcp = MCPServer("ClaimMate Digital Claims & Authority Bridge")


@mcp.tool()
def generate_poa(
    claimant_name: str,
    policy_number: str,
    tpa_name: str,
    scope: str = "INSURANCE_CLAIM_ADJUDICATION"
) -> dict:
    """Generate a digital Power of Attorney authorizing ClaimMate to represent a claimant."""

    poa_id = f"did:digio:poa:{uuid.uuid4().hex[:12]}"

    return {
        "status": "ISSUED",
        "poa_token": poa_id,
        "claimant": claimant_name,
        "authorized_representative": "ClaimMate AI (Autonomous Legal Proxy)",
        "counterparty": tpa_name,
        "scope": scope,
        "signed_at": datetime.now(timezone.utc).isoformat(),
        "valid_until": "2026-10-31T23:59:59Z",
        "verification_uri": f"https://mock.digio.in/v/{poa_id}"
    }


@mcp.tool()
def fetch_certified_bills(
    policy_number: str,
    consent_token: str
) -> dict:
    """Fetch authenticated certified hospital bills and supporting medical documents."""

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


@mcp.tool()
def submit_tpa_appeal(
    policy_number: str,
    denial_code: str,
    appeal_summary: str,
    evidence_urls: List[str],
    escalation_level: str = "TPA_INTERNAL"
) -> dict:
    """Submit an evidence-based appeal to the TPA."""

    if denial_code == "TIMEOUT_TEST":
        return {
            "success": False,
            "error": "TPA_GATEWAY_TIMEOUT",
            "message": "TPA Grievance Portal Gateway Timeout"
        }

    appeal_id = f"APL-{uuid.uuid4().hex[:8].upper()}"

    return {
        "success": True,
        "appeal_id": appeal_id,
        "status": "UNDER_REVIEW",
        "escalation_level": escalation_level,
        "turnaround_time_hours": 48,
        "submission_timestamp": datetime.now(timezone.utc).isoformat(),
        "acknowledgement": (
            f"Appeal for denial {denial_code} "
            f"formally logged under reference {appeal_id}."
        )
    }


@mcp.tool()
def create_chargeback_lock(
    order_id: str,
    amount_paise: int,
    dispute_reason: str
) -> dict:
    """Create a payment dispute lock to prevent further unauthorized settlement."""

    return {
        "status": "DISPUTE_RAISED",
        "dispute_ref": f"PL-DISP-{uuid.uuid4().hex[:6].upper()}",
        "order_id": order_id,
        "amount_inr": amount_paise / 100,
        "reason": dispute_reason,
        "mandate_frozen": True
    }


# AgenticOrg will connect to the MCP endpoint at /mcp.
security = TransportSecuritySettings(
    allowed_hosts=[
        "claimmate-digital-claims-bridge-pIj5hI7n4-claim-mate.vercel.app",
        "claimmate-digital-claims-bridge-pIj5hI7n4-claim-mate.vercel.app:*"
    ]
)

app = mcp.streamable_http_app(
    json_response=True,
    stateless_http=True,
    transport_security=security,
    streamable_http_path="/"
)
