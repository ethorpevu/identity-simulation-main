"""
Persona module for the Group Identity Simulation Platform.
Each persona is a carefully crafted system prompt grounded in social psychology research.
"""

from .conservative import CONSERVATIVE_PERSONA
from .libertarian import LIBERTARIAN_PERSONA
from .moderate import MODERATE_PERSONA
from .liberal import LIBERAL_PERSONA
from .progressive import PROGRESSIVE_PERSONA
from .cluster1 import CLUSTER1_PERSONA
from .cluster18 import CLUSTER18_PERSONA
from .cluster30 import CLUSTER30_PERSONA
from .cluster32 import CLUSTER32_PERSONA
from .cluster34 import CLUSTER34_PERSONA
from .cluster35 import CLUSTER35_PERSONA
from .cluster39 import CLUSTER39_PERSONA
from .cluster42 import CLUSTER42_PERSONA
from .cluster43 import CLUSTER43_PERSONA
from .cluster55 import CLUSTER55_PERSONA

PERSONAS = {
    "conservative": CONSERVATIVE_PERSONA,
    "libertarian": LIBERTARIAN_PERSONA,
    "moderate": MODERATE_PERSONA,
    "liberal": LIBERAL_PERSONA,
    "progressive": PROGRESSIVE_PERSONA,
    "cluster1": CLUSTER1_PERSONA,
    "cluster18": CLUSTER18_PERSONA,
    "cluster30": CLUSTER30_PERSONA,
    "cluster32": CLUSTER32_PERSONA,
    "cluster34": CLUSTER34_PERSONA,
    "cluster35": CLUSTER35_PERSONA,
    "cluster39": CLUSTER39_PERSONA,
    "cluster42": CLUSTER42_PERSONA,
    "cluster43": CLUSTER43_PERSONA,
    "cluster55": CLUSTER55_PERSONA,
}

__all__ = [
    "PERSONAS",
    "CONSERVATIVE_PERSONA",
    "LIBERTARIAN_PERSONA",
    "MODERATE_PERSONA",
    "LIBERAL_PERSONA",
    "PROGRESSIVE_PERSONA",
    "CLUSTER1_PERSONA",
    "CLUSTER18_PERSONA",
    "CLUSTER30_PERSONA",
    "CLUSTER32_PERSONA",
    "CLUSTER34_PERSONA",
    "CLUSTER35_PERSONA",
    "CLUSTER39_PERSONA",
    "CLUSTER42_PERSONA",
    "CLUSTER43_PERSONA",
    "CLUSTER55_PERSONA",
]
