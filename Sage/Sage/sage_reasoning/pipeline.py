"""
Reasoning Pipeline: Orchestrates the complete structured reasoning process.

Coordinates Structure, Reasoning, Scratchpad, and Presentation phases
with full traceability and verifiable tool use.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import json
import uuid

from .structure import StructurePhase, DSRPOntology
from .reasoning import ReasoningPhase, Hypothesis, FalsifiableTest, KillStep, TestResult
from .scratchpad import ScratchpadPhase, EvidenceSource, MemoryStore
from .presentation import PresentationPhase, SageVoice


@dataclass
class ReasoningTrace:
    """
    Complete trace of reasoning process for auditability.
    """
    
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_description: str = ""
    structure_phase: Optional[StructurePhase] = None
    reasoning_phase: Optional[ReasoningPhase] = None
    scratchpad_phase: Optional[ScratchpadPhase] = None
    presentation_phase: Optional[PresentationPhase] = None
    final_output: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize trace to dictionary."""
        return {
            "trace_id": self.trace_id,
            "task_description": self.task_description,
            "structure_phase": self.structure_phase.get_structure_summary() 
                if self.structure_phase else None,
            "reasoning_phase": self.reasoning_phase.get_reasoning_summary()
                if self.reasoning_phase else None,
            "scratchpad_phase": self.scratchpad_phase.get_scratchpad_summary()
                if self.scratchpad_phase else None,
            "final_output": self.final_output,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize trace to JSON."""
        return json.dumps(self.to_dict(), indent=indent, default=str)


class ReasoningPipeline:
    """
    Main pipeline orchestrator for structured reasoning.
    
    Coordinates all phases:
    1. Structure: Define ontology and boundaries
    2. Reasoning: Generate hypotheses and tests
    3. Scratchpad: Gather evidence and manage memory
    4. Presentation: Compose sage voice output
    """
    
    def __init__(self, 
                 tool_registry: Optional[Dict[str, Callable]] = None,
                 config: Optional[Dict[str, Any]] = None):
        """
        Initialize pipeline.
        
        Args:
            tool_registry: Dictionary mapping tool names to callable functions
            config: Configuration dictionary
        """
        self.tool_registry = tool_registry or {}
        self.config = config or {}
        self.traces: List[ReasoningTrace] = []
    
    def register_tool(self, name: str, tool_func: Callable) -> None:
        """Register a tool for use in scratchpad phase."""
        self.tool_registry[name] = tool_func
    
    def execute(self, task_description: str,
               context: Optional[Dict[str, Any]] = None) -> ReasoningTrace:
        """
        Execute the complete reasoning pipeline.
        
        Args:
            task_description: Description of the task to reason about
            context: Additional context for reasoning
            
        Returns:
            ReasoningTrace with complete reasoning process
        """
        context = context or {}
        trace = ReasoningTrace(task_description=task_description)
        
        try:
            # Phase 1: Structure
            trace.structure_phase = self._execute_structure_phase(
                task_description, context
            )
            
            # Phase 2: Reasoning
            trace.reasoning_phase = self._execute_reasoning_phase(
                task_description, trace.structure_phase, context
            )
            
            # Phase 3: Scratchpad
            trace.scratchpad_phase = self._execute_scratchpad_phase(
                trace.reasoning_phase, context
            )
            
            # Phase 4: Presentation
            trace.presentation_phase = self._execute_presentation_phase(
                trace.structure_phase,
                trace.reasoning_phase,
                trace.scratchpad_phase,
                context
            )
            
            # Compose final output
            trace.final_output = trace.presentation_phase.compose_output(
                trace.structure_phase,
                trace.reasoning_phase,
                trace.scratchpad_phase,
                context
            )
            
            trace.completed_at = datetime.now()
            self.traces.append(trace)
            
        except Exception as e:
            trace.metadata["error"] = str(e)
            trace.metadata["error_type"] = type(e).__name__
            raise
        
        return trace
    
    def _execute_structure_phase(self, task_description: str,
                                context: Dict[str, Any]) -> StructurePhase:
        """Execute structure phase."""
        phase = StructurePhase(task_description=task_description)
        phase.initialize_core_entities()
        
        # Add custom boundaries if specified
        if "boundaries" in context:
            for boundary_data in context["boundaries"]:
                from .structure import Boundary, BoundaryType
                boundary = Boundary(
                    boundary_type=BoundaryType(boundary_data.get("type", "conceptual")),
                    description=boundary_data.get("description", ""),
                    constraints=boundary_data.get("constraints", {}),
                    rationale=boundary_data.get("rationale"),
                )
                phase.ontology.add_boundary(boundary)
        
        return phase
    
    def _execute_reasoning_phase(self, task_description: str,
                                structure_phase: StructurePhase,
                                context: Dict[str, Any]) -> ReasoningPhase:
        """Execute reasoning phase."""
        phase = ReasoningPhase(task_id=structure_phase.task_description)
        
        # Generate rival hypotheses
        hypotheses = phase.generate_rival_hypotheses(
            task_description,
            min_hypotheses=context.get("min_hypotheses", 2)
        )
        
        # Design tests and kill-steps for each hypothesis
        for hypothesis in hypotheses:
            phase.design_tests(hypothesis)
            phase.specify_kill_steps(hypothesis)
        
        # If custom hypotheses provided, use those instead
        if "hypotheses" in context:
            phase.hypotheses = []
            for hyp_data in context["hypotheses"]:
                hypothesis = Hypothesis(
                    statement=hyp_data.get("statement", ""),
                    rationale=hyp_data.get("rationale", ""),
                    confidence=hyp_data.get("confidence", 0.5),
                )
                phase.design_tests(hypothesis)
                phase.specify_kill_steps(hypothesis)
                phase.hypotheses.append(hypothesis)
        
        return phase
    
    def _execute_scratchpad_phase(self, reasoning_phase: ReasoningPhase,
                                  context: Dict[str, Any]) -> ScratchpadPhase:
        """Execute scratchpad phase."""
        phase = ScratchpadPhase(task_id=reasoning_phase.task_id)
        
        # Gather evidence for each hypothesis
        for hypothesis in reasoning_phase.hypotheses:
            if hypothesis.status.value != "falsified":
                # Formulate search query
                query = phase.formulate_search_query(hypothesis, context)
                
                # Execute tool calls (if tools are registered)
                if self.tool_registry:
                    for tool_name, tool_func in self.tool_registry.items():
                        evidence = phase.execute_tool_call(
                            tool_name, query, tool_func
                        )
                        
                        # Decide on memory write
                        value_score = evidence.reliability_score
                        tags = [hypothesis.hypothesis_id, tool_name]
                        phase.decide_memory_write(
                            evidence, hypothesis.hypothesis_id,
                            value_score, tags
                        )
                
                # Analyze evidence and update hypothesis
                if phase.evidence_sources:
                    # Analyze evidence quality and relevance
                    evidence_analysis = self._analyze_evidence(
                        phase.evidence_sources, hypothesis
                    )
                    
                    # Execute tests with analyzed evidence
                    for test in hypothesis.tests:
                        # Calculate test value based on evidence analysis
                        if test.metric == "contradiction_score":
                            # Higher contradiction = higher test value (more likely to falsify)
                            test_value = evidence_analysis.get("contradiction_score", 0.3)
                        elif test.metric == "inconsistency_score":
                            # Higher inconsistency = higher test value
                            test_value = evidence_analysis.get("inconsistency_score", 0.2)
                        else:
                            # Default: use average reliability as inverse (lower reliability = higher falsification risk)
                            avg_reliability = evidence_analysis.get("avg_reliability", 0.7)
                            test_value = 1.0 - avg_reliability
                        
                        evidence_ids = [e.source_id for e in phase.evidence_sources]
                        test.execute(test_value, evidence_ids)
                        
                        # Update hypothesis confidence based on test results
                        if test.result == TestResult.FAIL:
                            hypothesis.confidence = max(0.0, hypothesis.confidence - 0.15)
                        elif test.result == TestResult.PASS:
                            hypothesis.confidence = min(1.0, hypothesis.confidence + 0.10)
                
                # Evaluate hypothesis
                hypothesis.evaluate()
        
        # Cleanup expired memory
        phase.memory_store.cleanup_expired()
        
        return phase
    
    def _execute_presentation_phase(self, structure_phase: StructurePhase,
                                   reasoning_phase: ReasoningPhase,
                                   scratchpad_phase: ScratchpadPhase,
                                   context: Dict[str, Any]) -> PresentationPhase:
        """Execute presentation phase."""
        phase = PresentationPhase(
            task_id=structure_phase.task_description,
            preserve_dissent=context.get("preserve_dissent", True),
            include_actionable_steps=context.get("include_actionable_steps", True),
        )
        
        # Adjust sage voice weights if specified
        if "sage_voice_weights" in context:
            weights = context["sage_voice_weights"]
            phase.sage_voice.therapist_weight = weights.get("therapist", 0.7)
            phase.sage_voice.scientist_weight = weights.get("scientist", 0.9)
            phase.sage_voice.generalist_weight = weights.get("generalist", 0.6)
            phase.sage_voice.engineer_weight = weights.get("engineer", 0.8)
            phase.sage_voice.philosopher_weight = weights.get("philosopher", 0.7)
            phase.sage_voice.artist_weight = weights.get("artist", 0.5)
            phase.sage_voice.comedian_weight = weights.get("comedian", 0.3)
        
        return phase
    
    def _analyze_evidence(self, evidence_sources: List[Any], 
                         hypothesis: Any) -> Dict[str, Any]:
        """
        Analyze evidence sources to extract metrics for hypothesis testing.
        
        Args:
            evidence_sources: List of EvidenceSource objects
            hypothesis: Hypothesis being tested
            
        Returns:
            Dictionary with analysis metrics
        """
        import re
        import json
        
        if not evidence_sources:
            return {
                "avg_reliability": 0.5,
                "contradiction_score": 0.0,
                "inconsistency_score": 0.0,
                "support_score": 0.5,
            }
        
        # Extract hypothesis keywords
        hyp_statement = hypothesis.statement.lower()
        hyp_keywords = set(re.findall(r'\b\w{4,}\b', hyp_statement))  # Words 4+ chars
        
        # Analyze each evidence source
        reliabilities = []
        contradictions = []
        supports = []
        inconsistencies = []
        
        for evidence in evidence_sources:
            reliabilities.append(evidence.reliability_score)
            
            # Try to parse result if it's JSON
            result_text = ""
            if evidence.result:
                if isinstance(evidence.result, str):
                    try:
                        result_data = json.loads(evidence.result)
                        # Extract text from structured data
                        if isinstance(result_data, dict):
                            result_text = " ".join([
                                str(v) for v in result_data.values() 
                                if isinstance(v, (str, int, float))
                            ]).lower()
                        else:
                            result_text = str(evidence.result).lower()
                    except (json.JSONDecodeError, TypeError):
                        result_text = str(evidence.result).lower()
                else:
                    result_text = str(evidence.result).lower()
            
            # Calculate contradiction score
            # Look for negative indicators
            negative_indicators = [
                'error', 'fail', 'wrong', 'incorrect', 'invalid', 'reject',
                'deny', 'refute', 'contradict', 'oppose', 'against', 'not',
                'cannot', 'unable', 'impossible', 'problem', 'issue', 'bug'
            ]
            
            contradiction_count = sum(
                1 for indicator in negative_indicators 
                if indicator in result_text
            )
            contradiction_score = min(1.0, contradiction_count / 5.0)  # Normalize
            contradictions.append(contradiction_score)
            
            # Calculate support score
            # Look for positive indicators and keyword matches
            positive_indicators = [
                'success', 'correct', 'valid', 'confirm', 'support', 'prove',
                'work', 'effective', 'good', 'best', 'recommend', 'suggest'
            ]
            
            support_count = sum(
                1 for indicator in positive_indicators 
                if indicator in result_text
            )
            
            # Check keyword overlap
            result_keywords = set(re.findall(r'\b\w{4,}\b', result_text))
            keyword_overlap = len(hyp_keywords & result_keywords)
            keyword_support = min(1.0, keyword_overlap / max(len(hyp_keywords), 1))
            
            support_score = min(1.0, (support_count / 5.0 + keyword_support) / 2.0)
            supports.append(support_score)
            
            # Calculate inconsistency score
            # Look for conflicting information or uncertainty
            uncertainty_indicators = [
                'maybe', 'perhaps', 'uncertain', 'unclear', 'ambiguous',
                'depends', 'varies', 'sometimes', 'might', 'could'
            ]
            
            inconsistency_count = sum(
                1 for indicator in uncertainty_indicators 
                if indicator in result_text
            )
            inconsistency_score = min(1.0, inconsistency_count / 3.0)
            inconsistencies.append(inconsistency_score)
        
        # Aggregate metrics
        return {
            "avg_reliability": sum(reliabilities) / len(reliabilities) if reliabilities else 0.5,
            "contradiction_score": sum(contradictions) / len(contradictions) if contradictions else 0.0,
            "inconsistency_score": sum(inconsistencies) / len(inconsistencies) if inconsistencies else 0.0,
            "support_score": sum(supports) / len(supports) if supports else 0.5,
            "evidence_count": len(evidence_sources),
        }
    
    def get_trace(self, trace_id: str) -> Optional[ReasoningTrace]:
        """Get a reasoning trace by ID."""
        for trace in self.traces:
            if trace.trace_id == trace_id:
                return trace
        return None
    
    def get_all_traces(self) -> List[ReasoningTrace]:
        """Get all reasoning traces."""
        return self.traces.copy()
    
    def export_trace(self, trace_id: str, filepath: str) -> None:
        """Export a trace to JSON file."""
        trace = self.get_trace(trace_id)
        if not trace:
            raise ValueError(f"Trace {trace_id} not found")
        
        with open(filepath, 'w') as f:
            f.write(trace.to_json())

