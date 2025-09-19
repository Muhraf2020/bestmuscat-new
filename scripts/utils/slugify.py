import re
import unicodedata


def slugify(name: str, neighborhood: str | None = None) -> str:
    """
    Convert a place name and optional neighborhood into a URL-safe slug.
    """
    base = f"{name} {neighborhood or ''}".strip().lower()
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode("ascii")
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return re.sub(r"-{2,}", "-", base)