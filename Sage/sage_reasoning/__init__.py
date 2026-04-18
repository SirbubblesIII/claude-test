"""
Sage-Conformant Intelligence: Structured Reasoning Module

A modular system for native structured reasoning with traceable,
falsifiable hypothesis testing and multi-faceted presentation.
"""

from .pipeline import ReasoningPipeline, ReasoningTrace
from .structure import StructurePhase, DSRPOntology, Boundary, Entity, BoundaryType, DetailLevel
from .reasoning import (
    ReasoningPhase, Hypothesis, FalsifiableTest, KillStep,
    HypothesisStatus, TestResult
)
from .scratchpad import (
    ScratchpadPhase, EvidenceSource, MemoryOperation, MemoryStore, MemoryEntry,
    EvidenceSourceType, MemoryOperationType
)
from .presentation import PresentationPhase, SageVoice, FacetContribution, FacetWeight

__version__ = "0.1.0"
__all__ = [
    "ReasoningPipeline",
    "ReasoningTrace",
    "StructurePhase",
    "DSRPOntology",
    "Boundary",
    "Entity",
    "BoundaryType",
    "DetailLevel",
    "ReasoningPhase",
    "Hypothesis",
    "FalsifiableTest",
    "KillStep",
    "HypothesisStatus",
    "TestResult",
    "ScratchpadPhase",
    "EvidenceSource",
    "MemoryOperation",
    "MemoryStore",
    "MemoryEntry",
    "EvidenceSourceType",
    "MemoryOperationType",
    "PresentationPhase",
    "SageVoice",
    "FacetContribution",
    "FacetWeight",
]

