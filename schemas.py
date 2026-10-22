"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NormActivationAnalysis(BaseModel):
    """Stern's Value-Belief-Norm chain (Behavioral Layers L3)."""
    consequences: str = Field(default="", description="Who or what they believe is threatened, and whether they credit it")
    responsibility: str = Field(default="", description="Who they hold responsible for causing and fixing it; efficacy")
    personal_norm: str = Field(default="", description="Whether a felt obligation activates, and how strongly")
    cost_response: str = Field(default="", description="Implied personal cost and any neutralization of the obligation")


class CulturalCognitionAnalysis(BaseModel):
    """Kahan's cultural cognition (Behavioral Layers L2)."""
    worldview_fit: str = Field(default="", description="Fit with their picture of how society should be ordered")
    solution_frame: str = Field(default="", description="Whether the implied solution is congenial, and its effect on belief in the facts")
    messenger_affinity: str = Field(default="", description="Perceived cultural identity and credibility of the messenger")
    likely_shift: str = Field(default="", description="Realistic movement after this message, including hardening")


class PersonaResponse(BaseModel):
    """Structured response from a persona analysis."""
    receptivity_score: int = Field(ge=0, le=100, description="0-100 receptivity score")
    initial_reaction: str = Field(description="Gut-level first impression")
    emotional_response: str = Field(description="Emotional feelings evoked")
    norm_activation: NormActivationAnalysis
    concerns: list[str] = Field(description="Specific objections or concerns")
    what_resonates: list[str] = Field(description="What works positively")
    barriers_to_persuasion: list[str] = Field(description="Why persuasion fails")
    trust_factors: str = Field(description="Source credibility assessment")
    suggested_reframings: list[str] = Field(description="How to improve the message")
    cultural_cognition: CulturalCognitionAnalysis
    authentic_voice_response: str = Field(description="200-word response in persona's voice")


class SimulationRequest(BaseModel):
    """Request to simulate message reception."""
    message: str = Field(min_length=1, description="The message to analyze")
    context_type: str = Field(default="general", description="Context type: tweet, policy_brief, speech, etc.")
    personas: list[str] = Field(default=["secular_progressive_egalitarian", "institutional_civic_moderate", "religious_free_market_conservative"],
                                 description="Which personas to simulate")


class PersonaResponseWithMeta(BaseModel):
    """Persona response with metadata."""
    persona_name: str
    response: PersonaResponse


class SimulationResponse(BaseModel):
    """Full simulation response."""
    simulation_id: int
    message: str
    context_type: str
    created_at: datetime
    responses: list[PersonaResponseWithMeta]


class SimulationSummary(BaseModel):
    """Summary of a simulation for listing."""
    id: int
    message: str
    context_type: str
    created_at: datetime
    response_count: int
    avg_receptivity: Optional[float]


class PersonaInfo(BaseModel):
    """Information about an available persona."""
    name: str
    display_name: str
    description: str
    moral_foundations_profile: dict[str, str] = {}
    cultural_cognition: str = ""
    key_triggers: list[str] = []
    key_bridges: list[str] = []


class ExportRequest(BaseModel):
    """Request for export."""
    format: str = Field(default="csv", description="Export format: csv or pdf")
