# Architecture Documentation

## Overview

The Sage-Conformant Intelligence structured reasoning module implements a four-phase pipeline for traceable, falsifiable reasoning with multi-faceted presentation.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ReasoningPipeline                         │
│                  (Main Orchestrator)                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Structure   │   │  Reasoning   │   │  Scratchpad  │
│    Phase     │──▶│    Phase     │──▶│    Phase     │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │ Presentation │
                   │    Phase     │
                   └──────────────┘
                            │
                            ▼
                   ┌──────────────┐
                   │ Final Output │
                   │ (Sage Voice)  │
                   └──────────────┘
```

## Phase Details

### 1. Structure Phase

**Purpose**: Define ontology, boundaries, and level of detail using DSRP framework.

**Key Components**:
- `DSRPOntology`: Distinctions, Systems, Relationships, Perspectives
- `Boundary`: Temporal, spatial, conceptual, domain, resource limits
- `Entity`: Core entities (task, hypothesis, evidence, memory, presentation)

**Output**: Structured ontology with defined boundaries and entities.

### 2. Reasoning Phase

**Purpose**: Generate rival hypotheses, design falsifiable tests, specify kill-steps.

**Key Components**:
- `Hypothesis`: Rival hypotheses with confidence scores
- `FalsifiableTest`: Tests designed to falsify hypotheses (Popperian approach)
- `KillStep`: Decision points with thresholds and reassessment triggers
- `HypothesisStatus`: Active, falsified, supported, inconclusive, suspended

**Output**: Set of hypotheses with tests and kill-steps.

### 3. Scratchpad Phase

**Purpose**: Gather evidence through tool calls, manage memory with lifecycle metadata.

**Key Components**:
- `EvidenceSource`: Timestamped, attributed evidence from tools
- `MemoryStore`: Manages memory entries with lifecycle tracking
- `MemoryOperation`: Explicit write/read/update/delete operations
- `MemoryEntry`: Value score, provenance, expiry, tags

**Output**: Evidence sources and memory entries.

### 4. Presentation Phase

**Purpose**: Compose output in "sage voice" balancing seven facets.

**Key Components**:
- `SageVoice`: Seven-facet composition engine
- Facets: Therapist, Scientist, Generalist, Engineer, Philosopher, Artist, Comedian

**Output**: Multi-faceted presentation preserving dissent and actionable steps.

## Data Flow

1. **Task Input** → Structure Phase
   - Task description analyzed
   - Ontology initialized
   - Boundaries defined

2. **Structure Output** → Reasoning Phase
   - Entities identified
   - Hypotheses generated
   - Tests designed

3. **Reasoning Output** → Scratchpad Phase
   - Search queries formulated
   - Tools executed
   - Evidence gathered
   - Memory updated

4. **Scratchpad Output** → Presentation Phase
   - Evidence analyzed
   - Hypotheses evaluated
   - Output composed

5. **Final Output** → User
   - Sage voice presentation
   - Traceable reasoning
   - Actionable steps

## Traceability

All reasoning is fully traceable through `ReasoningTrace`:

- Complete phase outputs
- Tool execution logs
- Memory operations
- Hypothesis evaluations
- Final composition

Traces can be exported to JSON for audit and analysis.

## Memory Management

Memory entries include:
- **Value Score**: Quality/relevance (0.0 to 1.0)
- **Provenance**: Source IDs and attribution chain
- **Expiry**: Automatic expiration with cleanup
- **Tags**: Categorization for querying

Memory operations are explicit and logged.

## Tool Integration

Tools are registered with the pipeline:

```python
pipeline.register_tool("tool_name", tool_function)
```

Tools are called with:
- Query/input
- Timestamp
- Attribution
- Results stored as EvidenceSource

## Sage Voice Facets

1. **Therapist** (0.7): Empathetic framing, supportive structure
2. **Scientist** (0.9): Rival hypotheses, uncertainty quantification
3. **Generalist** (0.6): Cross-domain analogies
4. **Engineer** (0.8): Concrete plans, edge cases
5. **Philosopher** (0.7): Explicit assumptions
6. **Artist** (0.5): Clarity through metaphor
7. **Comedian** (0.3): Appropriate levity

Weights are configurable per execution.

## Constraints Met

✅ **Traceable Reasoning**: Complete audit trail via ReasoningTrace
✅ **Verifiable Tool Use**: Timestamped, attributed tool calls
✅ **Memory Lifecycle**: Explicit metadata (value, provenance, expiry, tags)
✅ **Dissent Preservation**: Hypothesis dissent notes included
✅ **Actionable Steps**: Next actions extracted and presented

## Extensibility

The module is designed for extension:

- Custom hypothesis generators
- Additional tool types
- New presentation facets
- Alternative memory backends
- Custom boundary types

## Performance Considerations

- Memory cleanup runs automatically
- Expired entries are removed
- Traces can be exported/archived
- Tool calls are async-capable (structure supports it)

## Future Enhancements

- Parallel hypothesis evaluation
- Incremental reasoning updates
- Memory persistence backends
- Advanced uncertainty quantification
- Multi-agent reasoning coordination


