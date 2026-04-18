"""
Reasoning Phase: Hypothesis generation and falsifiable testing.

Generates rival hypotheses, designs tests, and specifies kill-steps
with thresholds and reassessment triggers.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable
from enum import Enum
from datetime import datetime
import uuid


class HypothesisStatus(Enum):
    """Status of a hypothesis in the reasoning process."""
    ACTIVE = "active"
    FALSIFIED = "falsified"
    SUPPORTED = "supported"
    INCONCLUSIVE = "inconclusive"
    SUSPENDED = "suspended"


class TestResult(Enum):
    """Result of a falsifiable test."""
    PASS = "pass"
    FAIL = "fail"
    INCONCLUSIVE = "inconclusive"
    ERROR = "error"


@dataclass
class FalsifiableTest:
    """
    A test designed to falsify a hypothesis.
    
    Based on Popperian falsificationism: a hypothesis is scientific
    if it can be falsified by empirical evidence.
    """
    
    test_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    hypothesis_id: str = ""
    description: str = ""
    test_procedure: str = ""
    expected_outcome_if_false: str = ""
    threshold: float = 0.5  # Threshold for falsification
    metric: str = "confidence"  # What metric to measure
    result: Optional[TestResult] = None
    actual_value: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    evidence_sources: List[str] = field(default_factory=list)
    
    def execute(self, actual_value: float, evidence_sources: List[str]) -> TestResult:
        """
        Execute the test and determine if hypothesis is falsified.
        
        Returns:
            TestResult indicating whether hypothesis is falsified
        """
        self.actual_value = actual_value
        self.evidence_sources = evidence_sources
        self.timestamp = datetime.now()
        
        # If actual value exceeds threshold, hypothesis is falsified
        if actual_value >= self.threshold:
            self.result = TestResult.FAIL
            return TestResult.FAIL
        elif actual_value < self.threshold * 0.3:  # Strong support
            self.result = TestResult.PASS
            return TestResult.PASS
        else:
            self.result = TestResult.INCONCLUSIVE
            return TestResult.INCONCLUSIVE
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize test to dictionary."""
        return {
            "test_id": self.test_id,
            "hypothesis_id": self.hypothesis_id,
            "description": self.description,
            "test_procedure": self.test_procedure,
            "expected_outcome_if_false": self.expected_outcome_if_false,
            "threshold": self.threshold,
            "metric": self.metric,
            "result": self.result.value if self.result else None,
            "actual_value": self.actual_value,
            "timestamp": self.timestamp.isoformat(),
            "evidence_sources": self.evidence_sources,
        }


@dataclass
class KillStep:
    """
    A kill-step that terminates a hypothesis if conditions are met.
    
    Kill-steps provide explicit decision points for hypothesis rejection
    or suspension, with reassessment triggers.
    """
    
    kill_step_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    hypothesis_id: str = ""
    condition: str = ""
    threshold: float = 0.0
    action: str = "suspend"  # suspend, reject, or reassess
    reassessment_trigger: Optional[str] = None
    triggered: bool = False
    timestamp: Optional[datetime] = None
    
    def check(self, value: float) -> bool:
        """
        Check if kill-step condition is met.
        
        Returns:
            True if kill-step should be triggered
        """
        if value >= self.threshold:
            self.triggered = True
            self.timestamp = datetime.now()
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize kill-step to dictionary."""
        return {
            "kill_step_id": self.kill_step_id,
            "hypothesis_id": self.hypothesis_id,
            "condition": self.condition,
            "threshold": self.threshold,
            "action": self.action,
            "reassessment_trigger": self.reassessment_trigger,
            "triggered": self.triggered,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


@dataclass
class Hypothesis:
    """
    A rival hypothesis with falsifiable tests and kill-steps.
    """
    
    hypothesis_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    statement: str = ""
    rationale: str = ""
    status: HypothesisStatus = HypothesisStatus.ACTIVE
    confidence: float = 0.5  # Initial confidence (0.0 to 1.0)
    tests: List[FalsifiableTest] = field(default_factory=list)
    kill_steps: List[KillStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    dissent_notes: List[str] = field(default_factory=list)
    
    def add_test(self, test: FalsifiableTest) -> None:
        """Add a falsifiable test to this hypothesis."""
        test.hypothesis_id = self.hypothesis_id
        self.tests.append(test)
    
    def add_kill_step(self, kill_step: KillStep) -> None:
        """Add a kill-step to this hypothesis."""
        kill_step.hypothesis_id = self.hypothesis_id
        self.kill_steps.append(kill_step)
    
    def update_status(self, new_status: HypothesisStatus) -> None:
        """Update hypothesis status."""
        self.status = new_status
        self.updated_at = datetime.now()
    
    def add_dissent(self, note: str) -> None:
        """Add a dissent note preserving alternative viewpoints."""
        self.dissent_notes.append(note)
    
    def evaluate(self) -> None:
        """
        Evaluate hypothesis based on test results and kill-steps.
        
        Updates status and confidence based on evidence.
        """
        # Check kill-steps first
        for kill_step in self.kill_steps:
            if kill_step.triggered:
                if kill_step.action == "reject":
                    self.update_status(HypothesisStatus.FALSIFIED)
                    return
                elif kill_step.action == "suspend":
                    self.update_status(HypothesisStatus.SUSPENDED)
                    return
        
        # Evaluate tests
        if not self.tests:
            self.update_status(HypothesisStatus.INCONCLUSIVE)
            return
        
        failed_tests = sum(1 for t in self.tests if t.result == TestResult.FAIL)
        passed_tests = sum(1 for t in self.tests if t.result == TestResult.PASS)
        total_tests = len(self.tests)
        
        if failed_tests > total_tests / 2:
            self.update_status(HypothesisStatus.FALSIFIED)
            self.confidence = max(0.0, self.confidence - 0.3)
        elif passed_tests > total_tests / 2:
            self.update_status(HypothesisStatus.SUPPORTED)
            self.confidence = min(1.0, self.confidence + 0.2)
        else:
            self.update_status(HypothesisStatus.INCONCLUSIVE)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize hypothesis to dictionary."""
        return {
            "hypothesis_id": self.hypothesis_id,
            "statement": self.statement,
            "rationale": self.rationale,
            "status": self.status.value,
            "confidence": self.confidence,
            "tests": [t.to_dict() for t in self.tests],
            "kill_steps": [k.to_dict() for k in self.kill_steps],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "dissent_notes": self.dissent_notes,
        }


@dataclass
class ReasoningPhase:
    """
    Reasoning Phase: Generates rival hypotheses and designs tests.
    """
    
    task_id: str = ""
    hypotheses: List[Hypothesis] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def generate_rival_hypotheses(self, task_description: str, 
                                  min_hypotheses: int = 2) -> List[Hypothesis]:
        """
        Generate at least two rival hypotheses for the task.
        
        Uses pattern analysis, keyword extraction, and heuristic-based
        generation to create meaningful rival hypotheses.
        """
        import re
        
        hypotheses = []
        task_lower = task_description.lower()
        
        # Extract key concepts and action verbs
        action_patterns = [
            r'\b(design|build|create|implement|develop|solve|optimize|improve|enhance|refactor|migrate|deploy|scale|secure|test|analyze|evaluate|choose|select|decide)\b',
            r'\b(should|must|need|require|want|can|could|would)\b',
        ]
        
        action_verbs = []
        for pattern in action_patterns:
            matches = re.findall(pattern, task_lower)
            action_verbs.extend(matches)
        
        # Extract domain keywords
        domain_keywords = []
        tech_keywords = [
            'system', 'architecture', 'api', 'database', 'authentication', 
            'security', 'performance', 'scalability', 'reliability', 
            'algorithm', 'framework', 'library', 'service', 'application',
            'infrastructure', 'deployment', 'monitoring', 'logging', 'caching'
        ]
        
        for keyword in tech_keywords:
            if keyword in task_lower:
                domain_keywords.append(keyword)
        
        # Extract question words to understand intent
        question_words = ['how', 'what', 'why', 'when', 'where', 'which']
        question_type = 'how'  # default
        for qw in question_words:
            if qw in task_lower:
                question_type = qw
                break
        
        # Generate hypotheses based on different approaches
        approach_patterns = []
        
        # Pattern 1: Standard/Traditional approach
        if 'design' in task_lower or 'architecture' in task_lower:
            approach_patterns.append({
                'type': 'standard',
                'statement': f"Use established industry-standard patterns and best practices for {task_description}",
                'rationale': "Leverages proven solutions with extensive community support and documentation",
                'confidence': 0.65,
            })
        
        # Pattern 2: Modern/Innovative approach
        if 'modern' in task_lower or 'new' in task_lower or 'latest' in task_lower:
            approach_patterns.append({
                'type': 'modern',
                'statement': f"Adopt cutting-edge technologies and modern architectural patterns for {task_description}",
                'rationale': "Takes advantage of latest innovations and improved capabilities",
                'confidence': 0.55,
            })
        else:
            # Add modern approach as alternative
            approach_patterns.append({
                'type': 'modern',
                'statement': f"Use modern, cloud-native approaches with microservices and containerization for {task_description}",
                'rationale': "Provides scalability, flexibility, and alignment with current industry trends",
                'confidence': 0.50,
            })
        
        # Pattern 3: Minimalist/Simple approach
        approach_patterns.append({
            'type': 'minimal',
            'statement': f"Implement a minimal, focused solution that addresses core requirements for {task_description}",
            'rationale': "Reduces complexity, faster to implement, easier to maintain and debug",
            'confidence': 0.60,
        })
        
        # Pattern 4: Hybrid/Comprehensive approach
        if 'scalable' in task_lower or 'enterprise' in task_lower or 'production' in task_lower:
            approach_patterns.append({
                'type': 'hybrid',
                'statement': f"Combine multiple approaches with layered architecture and redundancy for {task_description}",
                'rationale': "Provides robustness, fault tolerance, and accommodates future growth",
                'confidence': 0.70,
            })
        
        # Pattern 5: Security-first approach (if security-related keywords)
        if any(kw in task_lower for kw in ['security', 'auth', 'encrypt', 'secure', 'protect', 'access']):
            approach_patterns.append({
                'type': 'security',
                'statement': f"Prioritize security and compliance with defense-in-depth strategy for {task_description}",
                'rationale': "Ensures data protection, regulatory compliance, and reduces attack surface",
                'confidence': 0.75,
            })
        
        # Pattern 6: Performance-optimized approach
        if any(kw in task_lower for kw in ['performance', 'speed', 'fast', 'optimize', 'efficient', 'latency']):
            approach_patterns.append({
                'type': 'performance',
                'statement': f"Optimize for performance and efficiency with caching, async processing, and resource optimization for {task_description}",
                'rationale': "Maximizes throughput, minimizes latency, and optimizes resource utilization",
                'confidence': 0.70,
            })
        
        # Pattern 7: Cost-effective approach
        if 'cost' in task_lower or 'budget' in task_lower or 'cheap' in task_lower:
            approach_patterns.append({
                'type': 'cost',
                'statement': f"Minimize costs using open-source solutions and efficient resource allocation for {task_description}",
                'rationale': "Reduces operational expenses while maintaining acceptable performance",
                'confidence': 0.60,
            })
        
        # If no specific patterns matched, create generic rival hypotheses
        if len(approach_patterns) < min_hypotheses:
            # Generic hypothesis 1: Proactive/Comprehensive
            approach_patterns.append({
                'type': 'comprehensive',
                'statement': f"Implement a comprehensive solution with full feature set and extensive error handling for {task_description}",
                'rationale': "Addresses all requirements upfront, reduces technical debt, provides better user experience",
                'confidence': 0.65,
            })
            
            # Generic hypothesis 2: Iterative/Agile
            approach_patterns.append({
                'type': 'iterative',
                'statement': f"Use iterative development with MVP first, then enhance based on feedback for {task_description}",
                'rationale': "Faster time to market, validates assumptions early, adapts to changing requirements",
                'confidence': 0.60,
            })
        
        # Select top hypotheses, ensuring diversity
        selected_patterns = []
        seen_types = set()
        
        # Prioritize by confidence and diversity
        sorted_patterns = sorted(approach_patterns, key=lambda x: x['confidence'], reverse=True)
        
        for pattern in sorted_patterns:
            if len(selected_patterns) >= max(min_hypotheses, 3):  # Generate at least 3 if possible
                break
            if pattern['type'] not in seen_types or len(selected_patterns) < min_hypotheses:
                selected_patterns.append(pattern)
                seen_types.add(pattern['type'])
        
        # Create Hypothesis objects
        for i, pattern in enumerate(selected_patterns, 1):
            hyp = Hypothesis(
                statement=pattern['statement'],
                rationale=pattern['rationale'],
                confidence=pattern['confidence'],
            )
            hypotheses.append(hyp)
        
        # Ensure we have at least min_hypotheses
        while len(hypotheses) < min_hypotheses:
            hyp = Hypothesis(
                statement=f"Alternative approach {len(hypotheses) + 1}: {task_description}",
                rationale="Alternative perspective based on different priorities or constraints",
                confidence=0.45,
            )
            hypotheses.append(hyp)
        
        self.hypotheses = hypotheses
        return hypotheses
    
    def design_tests(self, hypothesis: Hypothesis) -> List[FalsifiableTest]:
        """
        Design falsifiable tests for a hypothesis.
        
        Returns:
            List of tests that could falsify the hypothesis
        """
        tests = []
        
        # Test 1: Empirical validation
        test1 = FalsifiableTest(
            description=f"Empirical validation of: {hypothesis.statement}",
            test_procedure="Gather empirical evidence and measure against expected outcomes",
            expected_outcome_if_false="Evidence contradicts hypothesis predictions",
            threshold=0.7,
            metric="contradiction_score",
        )
        tests.append(test1)
        
        # Test 2: Logical consistency
        test2 = FalsifiableTest(
            description=f"Logical consistency check for: {hypothesis.statement}",
            test_procedure="Check for internal contradictions and logical fallacies",
            expected_outcome_if_false="Logical inconsistencies found",
            threshold=0.5,
            metric="inconsistency_score",
        )
        tests.append(test2)
        
        for test in tests:
            hypothesis.add_test(test)
        
        return tests
    
    def specify_kill_steps(self, hypothesis: Hypothesis) -> List[KillStep]:
        """
        Specify kill-steps with thresholds and reassessment triggers.
        """
        kill_steps = []
        
        # Kill-step 1: Confidence threshold
        kill_step1 = KillStep(
            condition="Confidence drops below threshold",
            threshold=0.2,
            action="suspend",
            reassessment_trigger="New evidence emerges that could increase confidence",
        )
        kill_steps.append(kill_step1)
        
        # Kill-step 2: Multiple test failures
        kill_step2 = KillStep(
            condition="Multiple falsifiable tests fail",
            threshold=0.6,  # 60% of tests fail
            action="reject",
            reassessment_trigger="New testing methodology becomes available",
        )
        kill_steps.append(kill_step2)
        
        for kill_step in kill_steps:
            hypothesis.add_kill_step(kill_step)
        
        return kill_steps
    
    def get_reasoning_summary(self) -> Dict[str, Any]:
        """Get a summary of the reasoning phase."""
        return {
            "task_id": self.task_id,
            "hypotheses": [h.to_dict() for h in self.hypotheses],
            "timestamp": self.timestamp.isoformat(),
            "active_count": sum(1 for h in self.hypotheses 
                              if h.status == HypothesisStatus.ACTIVE),
            "falsified_count": sum(1 for h in self.hypotheses 
                                 if h.status == HypothesisStatus.FALSIFIED),
        }

