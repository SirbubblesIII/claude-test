# Sage-Conformant Intelligence: Structured Reasoning Module

A modular system for native structured reasoning with traceable, falsifiable hypothesis testing and multi-faceted presentation.

## Overview

This module implements a four-phase reasoning pipeline:

1. **Structure Phase**: Defines ontology, boundaries, and level of detail using DSRP (Distinctions, Systems, Relationships, Perspectives)
2. **Reasoning Phase**: Generates rival hypotheses, designs falsifiable tests, and specifies kill-steps
3. **Scratchpad Phase**: Gathers evidence through tool calls, manages memory with lifecycle metadata
4. **Presentation Phase**: Composes output in "sage voice" balancing seven facets

## Features

- **Traceable Reasoning**: Complete audit trail of all reasoning steps
- **Falsifiable Testing**: Popperian approach to hypothesis validation
- **Memory Management**: Explicit lifecycle metadata (value scores, provenance, expiry, tags)
- **Multi-faceted Presentation**: Balances seven perspectives (Therapist, Scientist, Generalist, Engineer, Philosopher, Artist, Comedian)
- **Modular Design**: Reusable components for each phase

## Installation

```bash
# Clone or copy the sage_reasoning module to your project
```

## Quick Start

```python
from sage_reasoning import ReasoningPipeline

# Initialize pipeline
pipeline = ReasoningPipeline()

# Register tools for evidence gathering
def my_search_tool(query: str, **kwargs):
    # Your tool implementation
    return evidence_result

pipeline.register_tool("search", my_search_tool)

# Execute reasoning
task = "How should we solve problem X?"
context = {
    "min_hypotheses": 2,
    "preserve_dissent": True,
    "include_actionable_steps": True,
}

trace = pipeline.execute(task, context)
print(trace.final_output)
```

## Architecture

### Structure Phase (`structure.py`)

- **DSRPOntology**: Defines entities, systems, relationships, and perspectives
- **Boundaries**: Temporal, spatial, conceptual, domain, and resource limits
- **Detail Levels**: Macro, meso, and micro granularity

### Reasoning Phase (`reasoning.py`)

- **Hypothesis**: Rival hypotheses with confidence scores
- **FalsifiableTest**: Tests designed to falsify hypotheses
- **KillStep**: Decision points for hypothesis rejection/suspension
- **Status Tracking**: Active, falsified, supported, inconclusive, suspended

### Scratchpad Phase (`scratchpad.py`)

- **EvidenceSource**: Timestamped, attributed evidence from tools
- **MemoryStore**: Manages memory entries with lifecycle metadata
- **MemoryOperation**: Explicit write/read/update/delete operations
- **Tool Integration**: Executes registered tools with attribution

### Presentation Phase (`presentation.py`)

- **SageVoice**: Seven-facet composition engine
- **Facets**:
  - **Therapist**: Empathetic framing
  - **Scientist**: Rival hypotheses, uncertainty quantification
  - **Generalist**: Cross-domain analogies
  - **Engineer**: Concrete plans with edge cases
  - **Philosopher**: Explicit assumptions
  - **Artist**: Clarity through metaphor
  - **Comedian**: Appropriate levity

## Usage Examples

See `examples/basic_usage.py` for a complete example.

## Traceability

All reasoning is fully traceable:

```python
# Get trace
trace = pipeline.get_trace(trace_id)

# Export to JSON
pipeline.export_trace(trace_id, "trace.json")

# Access individual phases
structure = trace.structure_phase
reasoning = trace.reasoning_phase
scratchpad = trace.scratchpad_phase
presentation = trace.presentation_phase
```

## Memory Management

Memory entries include:
- **Value Score**: Quality/relevance (0.0 to 1.0)
- **Provenance**: Source IDs and attribution
- **Expiry**: Automatic expiration with cleanup
- **Tags**: Categorization for querying

```python
# Query memory
entries = scratchpad.memory_store.query(
    tags=["hypothesis_123"],
    min_score=0.5
)
```

## Configuration

Customize the pipeline behavior:

```python
context = {
    "min_hypotheses": 3,
    "preserve_dissent": True,
    "include_actionable_steps": True,
    "sage_voice_weights": {
        "therapist": 0.8,
        "scientist": 0.9,
        "generalist": 0.7,
        "engineer": 0.8,
        "philosopher": 0.6,
        "artist": 0.5,
        "comedian": 0.3,
    },
    "boundaries": [
        {
            "type": "temporal",
            "description": "Reasoning within 1 hour window",
            "constraints": {"max_duration": "1h"},
        },
    ],
}
```

## Constraints

- All reasoning is traceable
- Tool use is real and verifiable
- Memory has explicit lifecycle metadata
- Output preserves dissent and includes actionable steps

## License

[Specify your license here]

## Contributing

[Contributing guidelines]

