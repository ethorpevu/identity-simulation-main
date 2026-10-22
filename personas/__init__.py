"""
Persona module for the Group Identity Simulation Platform.
Six ideological groups, three personas each. Each persona file in ./generic is loaded once
at import and used verbatim as a system prompt (minus the researcher-only final section).
"""

from pathlib import Path

_DIR = Path(__file__).parent / "generic"
_CUT = "BEHIND-THE-SCENES CONTEXT"  # researcher notes; must not reach the model

GROUPS = [
    ("secular_progressive_egalitarian", "Secular Progressive Egalitarian",
     "Secular, egalitarian and communitarian, pro-science and pro-media, and distrustful of police, the military, churches and big business."),
    ("institutional_civic_moderate", "Institutional Civic Moderate",
     "Moderately religious and the most trusting of other people and institutions, and most responsive to expert messengers."),
    ("disaffected_distruster", "Disaffected Distruster",
     "Low trust in people, institutions and science, fatalistic, and suspicious of every messenger regardless of party."),
    ("secular_market_nationalist", "Secular Market Nationalist",
     "Secular, market-minded and nationalist, fairly optimistic about science and innovation, and resistant to mandates."),
    ("religious_communitarian_traditionalist", "Religious Communitarian Traditionalist",
     "Religious and traditional but wary of markets, and drawn to stewardship and community framing."),
    ("religious_free_market_conservative", "Religious Free-Market Conservative",
     "The most religious and most pro-market group, hierarchical and individualist, with the strongest identity-protective dismissal of climate risk."),
]

GROUP_MEMBERS = {slug: [f"{slug}_{n}" for n in (1, 2, 3)] for slug, _, _ in GROUPS}


def _load(key: str) -> dict:
    text = (_DIR / f"{key}.txt").read_text(encoding="utf-8")
    return {"name": key, "system_prompt": text.split(_CUT)[0].rstrip()}


# keyed "<group_slug>_<1|2|3>"; filenames are the same with the original capitalisation
_FILES = {p.stem.lower(): p.stem for p in _DIR.glob("*.txt")}
PERSONAS = {k: _load(_FILES[k]) for keys in GROUP_MEMBERS.values() for k in keys}
