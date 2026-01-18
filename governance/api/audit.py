import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


AUDIT_LOG_PATH = Path("audit_logs")
AUDIT_LOG_PATH.mkdir(exist_ok=True)


def _hash_payload(payload: Dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def write_audit_log(event_type: str, payload: Dict[str, Any], actor: str = "system") -> Dict[str, Any]:
    timestamp = datetime.utcnow().isoformat()
    payload_hash = _hash_payload(payload)

    record = {
        "timestamp": timestamp,
        "event_type": event_type,
        "actor": actor,
        "payload_hash": payload_hash,
        "payload": payload,
    }

    filename = AUDIT_LOG_PATH / f"audit_{timestamp.replace(':', '-')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    return record
