from typing import List, Dict, Any, Optional
from datetime import datetime


def make_prov(provider: str, place_id: Optional[str], fields: List[str]) -> Dict[str, Any]:
    """
    Construct a provenance entry for a set of fields collected from a provider.
    """
    return {
        "provider": provider,
        "place_id": place_id,
        "fields": fields,
        "terms_url": None,
        "collected_at": datetime.utcnow().strftime("%Y-%m-%d")
    }