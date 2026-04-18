"""
Structure Phase: DSRP-based ontology and boundary definition.

DSRP (Distinctions, Systems, Relationships, Perspectives) provides
a framework for defining the reasoning domain's structure.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum
from datetime import datetime
import json


class BoundaryType(Enum):
    """Types of boundaries in the reasoning space."""
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    CONCEPTUAL = "conceptual"
    DOMAIN = "domain"
    RESOURCE = "resource"


class DetailLevel(Enum):
    """Levels of detail for reasoning."""
    MACRO = "macro"  # High-level overview
    MESO = "meso"    # Intermediate detail
    MICRO = "micro"  # Fine-grained detail


@dataclass
class Boundary:
    """Represents a boundary in the reasoning space."""
    boundary_type: BoundaryType
    description: str
    constraints: Dict[str, Any] = field(default_factory=dict)
    rationale: Optional[str] = None


@dataclass
class Entity:
    """Core entity in the reasoning ontology."""
    name: str
    entity_type: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    relationships: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DSRPOntology:
    """
    DSRP-based ontology defining the reasoning structure.
    
    DSRP Components:
    - Distinctions: What entities are distinguished
    - Systems: How entities are grouped
    - Relationships: How entities connect
    - Perspectives: Different viewpoints on the same structure
    """
    
    # Distinctions: Key entities that are distinguished
    distinctions: List[Entity] = field(default_factory=list)
    
    # Systems: Groupings of entities
    systems: Dict[str, List[str]] = field(default_factory=dict)
    
    # Relationships: Connections between entities
    relationships: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    # Perspectives: Different viewpoints
    perspectives: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    
    # Boundaries: Limits of the reasoning space
    boundaries: List[Boundary] = field(default_factory=list)
    
    # Level of detail
    detail_level: DetailLevel = DetailLevel.MESO
    
    def add_distinction(self, entity: Entity) -> None:
        """Add a distinguished entity."""
        self.distinctions.append(entity)
    
    def create_system(self, system_name: str, entity_names: List[str]) -> None:
        """Group entities into a system."""
        self.systems[system_name] = entity_names
    
    def add_relationship(self, from_entity: str, to_entity: str, 
                       relationship_type: str) -> None:
        """Add a relationship between entities."""
        if from_entity not in self.relationships:
            self.relationships[from_entity] = {}
        self.relationships[from_entity][to_entity] = relationship_type
    
    def add_perspective(self, perspective_name: str, 
                       viewpoint: Dict[str, Any]) -> None:
        """Add a perspective on the ontology."""
        self.perspectives[perspective_name] = viewpoint
    
    def add_boundary(self, boundary: Boundary) -> None:
        """Add a boundary to the reasoning space."""
        self.boundaries.append(boundary)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize ontology to dictionary."""
        return {
            "distinctions": [
                {
                    "name": e.name,
                    "type": e.entity_type,
                    "attributes": e.attributes,
                    "relationships": e.relationships,
                    "metadata": e.metadata,
                }
                for e in self.distinctions
            ],
            "systems": self.systems,
            "relationships": self.relationships,
            "perspectives": self.perspectives,
            "boundaries": [
                {
                    "type": b.boundary_type.value,
                    "description": b.description,
                    "constraints": b.constraints,
                    "rationale": b.rationale,
                }
                for b in self.boundaries
            ],
            "detail_level": self.detail_level.value,
        }


@dataclass
class StructurePhase:
    """
    Structure Phase: Defines ontology, boundaries, and level of detail.
    """
    
    task_description: str
    ontology: DSRPOntology = field(default_factory=DSRPOntology)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def initialize_core_entities(self) -> None:
        """Initialize core entities for structured reasoning."""
        # Task entity
        task_entity = Entity(
            name="task",
            entity_type="primary",
            attributes={
                "description": self.task_description,
                "complexity": "variable",
            },
            metadata={"created": self.timestamp.isoformat()},
        )
        
        # Hypothesis entity
        hypothesis_entity = Entity(
            name="hypothesis",
            entity_type="reasoning",
            attributes={
                "falsifiable": True,
                "testable": True,
            },
        )
        
        # Evidence source entity
        evidence_entity = Entity(
            name="evidence_source",
            entity_type="data",
            attributes={
                "verifiable": True,
                "timestamped": True,
            },
        )
        
        # Memory operation entity
        memory_entity = Entity(
            name="memory_operation",
            entity_type="storage",
            attributes={
                "lifecycle_managed": True,
                "metadata_enriched": True,
            },
        )
        
        # Presentation format entity
        presentation_entity = Entity(
            name="presentation_format",
            entity_type="output",
            attributes={
                "multi_faceted": True,
                "traceable": True,
            },
        )
        
        # Add distinctions
        for entity in [task_entity, hypothesis_entity, evidence_entity, 
                      memory_entity, presentation_entity]:
            self.ontology.add_distinction(entity)
        
        # Create systems
        self.ontology.create_system(
            "reasoning_entities",
            ["task", "hypothesis"]
        )
        self.ontology.create_system(
            "data_entities",
            ["evidence_source", "memory_operation"]
        )
        self.ontology.create_system(
            "output_entities",
            ["presentation_format"]
        )
        
        # Add relationships
        self.ontology.add_relationship("task", "hypothesis", "generates")
        self.ontology.add_relationship("hypothesis", "evidence_source", "tests_with")
        self.ontology.add_relationship("evidence_source", "memory_operation", "feeds")
        self.ontology.add_relationship("memory_operation", "presentation_format", "informs")
        
        # Add boundaries
        temporal_boundary = Boundary(
            boundary_type=BoundaryType.TEMPORAL,
            description="Reasoning occurs within a bounded time window",
            constraints={"max_duration": "configurable"},
            rationale="Prevents infinite reasoning loops",
        )
        
        domain_boundary = Boundary(
            boundary_type=BoundaryType.DOMAIN,
            description="Reasoning is scoped to relevant domains",
            constraints={"scope": "task-dependent"},
            rationale="Maintains focus and relevance",
        )
        
        self.ontology.add_boundary(temporal_boundary)
        self.ontology.add_boundary(domain_boundary)
    
    def get_structure_summary(self) -> Dict[str, Any]:
        """Get a summary of the structure phase."""
        return {
            "task": self.task_description,
            "ontology": self.ontology.to_dict(),
            "timestamp": self.timestamp.isoformat(),
        }

