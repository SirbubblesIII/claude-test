"""
Presentation Phase: Multi-faceted sage voice composition.

Balances seven facets:
- Therapist: empathetic framing
- Scientist: rival hypotheses, uncertainty quantification
- Generalist: cross-domain analogies
- Engineer: concrete plans with edge cases
- Philosopher: explicit assumptions
- Artist: clarity through metaphor
- Comedian: appropriate levity
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class FacetWeight(Enum):
    """Relative weight of each facet in presentation."""
    LOW = 0.2
    MEDIUM = 0.5
    HIGH = 0.8
    DOMINANT = 1.0


@dataclass
class FacetContribution:
    """Contribution from a specific facet."""
    facet_name: str
    content: str
    weight: float = 0.5
    rationale: Optional[str] = None


@dataclass
class SageVoice:
    """
    Sage voice with seven facets balanced in presentation.
    """
    
    # Facet weights (0.0 to 1.0)
    therapist_weight: float = 0.7
    scientist_weight: float = 0.9
    generalist_weight: float = 0.6
    engineer_weight: float = 0.8
    philosopher_weight: float = 0.7
    artist_weight: float = 0.5
    comedian_weight: float = 0.3
    
    def therapist_frame(self, content: str, context: Dict[str, Any]) -> str:
        """
        Therapist facet: Empathetic framing.
        
        Acknowledges difficulty, validates concerns, provides
        supportive structure.
        """
        framing = ""
        if context.get("uncertainty", 0) > 0.5:
            framing = "I understand this may feel uncertain or complex. "
        if context.get("difficulty", False):
            framing += "Let's approach this step by step, acknowledging "
            framing += "the challenges we're facing. "
        return framing + content
    
    def scientist_frame(self, hypotheses: List[Any], 
                       uncertainty: float) -> str:
        """
        Scientist facet: Rival hypotheses and uncertainty quantification.
        
        Presents multiple hypotheses, quantifies uncertainty,
        shows falsification process.
        """
        content = "From a scientific perspective, we have "
        content += f"{len(hypotheses)} rival hypotheses to consider:\n\n"
        
        for i, hyp in enumerate(hypotheses, 1):
            status_emoji = {
                "active": "🔬",
                "supported": "✅",
                "falsified": "❌",
                "inconclusive": "❓",
            }.get(hyp.status.value, "🔍")
            
            content += f"{status_emoji} Hypothesis {i}: {hyp.statement}\n"
            content += f"   Confidence: {hyp.confidence:.2f}\n"
            content += f"   Status: {hyp.status.value}\n"
            if hyp.dissent_notes:
                content += f"   Note: {hyp.dissent_notes[0]}\n"
            content += "\n"
        
        content += f"\nUncertainty level: {uncertainty:.2f} "
        content += f"({'high' if uncertainty > 0.7 else 'moderate' if uncertainty > 0.4 else 'low'})\n"
        
        return content
    
    def generalist_frame(self, content: str, 
                        analogies: List[Dict[str, str]]) -> str:
        """
        Generalist facet: Cross-domain analogies.
        
        Uses analogies from different domains to illuminate concepts.
        """
        if not analogies:
            return content
        
        analogy_text = "\n\nDrawing from other domains:\n"
        for analogy in analogies:
            analogy_text += f"• {analogy.get('domain', 'Unknown')}: "
            analogy_text += f"{analogy.get('analogy', '')}\n"
        
        return content + analogy_text
    
    def engineer_frame(self, plan: Dict[str, Any], 
                      edge_cases: List[str]) -> str:
        """
        Engineer facet: Concrete plans with edge cases.
        
        Provides actionable steps and considers failure modes.
        """
        content = "Implementation plan:\n\n"
        
        steps = plan.get("steps", [])
        for i, step in enumerate(steps, 1):
            content += f"{i}. {step}\n"
        
        if edge_cases:
            content += "\nEdge cases to consider:\n"
            for case in edge_cases:
                content += f"  ⚠️  {case}\n"
        
        if plan.get("next_actions"):
            content += "\nNext actions:\n"
            for action in plan["next_actions"]:
                content += f"  → {action}\n"
        
        return content
    
    def philosopher_frame(self, assumptions: List[str],
                         presuppositions: List[str]) -> str:
        """
        Philosopher facet: Explicit assumptions.
        
        Makes implicit assumptions explicit, questions presuppositions.
        """
        content = "Underlying assumptions:\n\n"
        
        for assumption in assumptions:
            content += f"• {assumption}\n"
        
        if presuppositions:
            content += "\nPresuppositions to question:\n"
            for presup in presuppositions:
                content += f"  ? {presup}\n"
        
        return content
    
    def artist_frame(self, content: str, 
                    metaphors: List[Dict[str, str]]) -> str:
        """
        Artist facet: Clarity through metaphor.
        
        Uses metaphors and imagery to make abstract concepts concrete.
        """
        if not metaphors:
            return content
        
        metaphor_text = "\n\nTo illuminate this:\n"
        for metaphor in metaphors:
            metaphor_text += f"  \"{metaphor.get('metaphor', '')}\" "
            metaphor_text += f"({metaphor.get('source', '')})\n"
        
        return content + metaphor_text
    
    def comedian_frame(self, content: str, 
                      levity_points: List[str]) -> str:
        """
        Comedian facet: Appropriate levity.
        
        Adds light touches where appropriate without undermining gravity.
        """
        if not levity_points or len(levity_points) == 0:
            return content
        
        # Only add levity if appropriate (not for serious failures, etc.)
        if len(levity_points) > 0:
            # Add a light touch at the end
            levity = "\n\n" + levity_points[0]
            return content + levity
        
        return content
    
    def compose(self, contributions: Dict[str, str],
               context: Dict[str, Any]) -> str:
        """
        Compose final output balancing all seven facets.
        """
        sections = []
        
        # Therapist: Empathetic opening
        if "therapist" in contributions:
            therapist_content = self.therapist_frame(
                contributions["therapist"],
                context
            )
            sections.append(("Therapist", therapist_content, 
                           self.therapist_weight))
        
        # Scientist: Hypothesis presentation
        if "scientist" in contributions:
            hypotheses = context.get("hypotheses", [])
            uncertainty = context.get("uncertainty", 0.5)
            scientist_content = self.scientist_frame(hypotheses, uncertainty)
            sections.append(("Scientist", scientist_content,
                           self.scientist_weight))
        
        # Generalist: Analogies
        if "generalist" in contributions:
            analogies = context.get("analogies", [])
            generalist_content = self.generalist_frame(
                contributions["generalist"],
                analogies
            )
            sections.append(("Generalist", generalist_content,
                           self.generalist_weight))
        
        # Engineer: Plans
        if "engineer" in contributions:
            plan = context.get("plan", {})
            edge_cases = context.get("edge_cases", [])
            engineer_content = self.engineer_frame(plan, edge_cases)
            sections.append(("Engineer", engineer_content,
                           self.engineer_weight))
        
        # Philosopher: Assumptions
        if "philosopher" in contributions:
            assumptions = context.get("assumptions", [])
            presuppositions = context.get("presuppositions", [])
            philosopher_content = self.philosopher_frame(
                assumptions, presuppositions
            )
            sections.append(("Philosopher", philosopher_content,
                           self.philosopher_weight))
        
        # Artist: Metaphors
        if "artist" in contributions:
            metaphors = context.get("metaphors", [])
            artist_content = self.artist_frame(
                contributions["artist"],
                metaphors
            )
            sections.append(("Artist", artist_content, self.artist_weight))
        
        # Comedian: Levity
        if "comedian" in contributions:
            levity_points = context.get("levity_points", [])
            comedian_content = self.comedian_frame(
                contributions.get("comedian", ""),
                levity_points
            )
            sections.append(("Comedian", comedian_content,
                           self.comedian_weight))
        
        # Combine sections weighted by importance
        final_output = ""
        for facet_name, content, weight in sections:
            if weight > 0.3:  # Only include significant contributions
                final_output += f"\n{'='*60}\n"
                final_output += f"{facet_name.upper()} PERSPECTIVE\n"
                final_output += f"{'='*60}\n\n"
                final_output += content
                final_output += "\n"
        
        return final_output.strip()


@dataclass
class PresentationPhase:
    """
    Presentation Phase: Composes output in sage voice.
    """
    
    task_id: str = ""
    sage_voice: SageVoice = field(default_factory=SageVoice)
    timestamp: datetime = field(default_factory=datetime.now)
    preserve_dissent: bool = True
    include_actionable_steps: bool = True
    
    def compose_output(self, structure_phase: Any,
                      reasoning_phase: Any,
                      scratchpad_phase: Any,
                      context: Dict[str, Any]) -> str:
        """
        Compose the final output balancing all seven facets.
        
        Args:
            structure_phase: Results from structure phase
            reasoning_phase: Results from reasoning phase
            scratchpad_phase: Results from scratchpad phase
            context: Additional context for composition
            
        Returns:
            Composed output in sage voice
        """
        contributions = {}
        
        # Generate sophisticated contributions from each phase
        if reasoning_phase and reasoning_phase.hypotheses:
            # Scientist contribution: Detailed hypothesis analysis
            hyp_summary = self._generate_hypothesis_summary(reasoning_phase.hypotheses)
            contributions["scientist"] = hyp_summary
            
            # Therapist contribution: Empathetic framing of the reasoning journey
            therapist_msg = self._generate_therapist_message(reasoning_phase, context)
            contributions["therapist"] = therapist_msg
        
        if scratchpad_phase and scratchpad_phase.evidence_sources:
            # Generalist contribution: Cross-domain insights from evidence
            generalist_msg = self._generate_generalist_insights(
                scratchpad_phase.evidence_sources, context
            )
            contributions["generalist"] = generalist_msg
            
            # Engineer contribution: Technical implementation insights
            engineer_msg = self._generate_engineer_insights(
                scratchpad_phase, reasoning_phase
            )
            contributions["engineer"] = engineer_msg
        
        # Build context for composition
        composition_context = {
            "hypotheses": reasoning_phase.hypotheses if reasoning_phase else [],
            "uncertainty": self._calculate_uncertainty(reasoning_phase),
            "difficulty": context.get("difficulty", False),
            "analogies": context.get("analogies", []),
            "plan": self._extract_plan(reasoning_phase, scratchpad_phase),
            "edge_cases": context.get("edge_cases", []),
            "assumptions": self._extract_assumptions(structure_phase),
            "presuppositions": context.get("presuppositions", []),
            "metaphors": context.get("metaphors", []),
            "levity_points": context.get("levity_points", []),
        }
        
        # Compose output
        output = self.sage_voice.compose(contributions, composition_context)
        
        # Add dissent if preserved
        if self.preserve_dissent and reasoning_phase:
            dissent_section = self._format_dissent(reasoning_phase)
            if dissent_section:
                output += "\n\n" + dissent_section
        
        # Add actionable steps
        if self.include_actionable_steps:
            actionable_steps = self._extract_actionable_steps(
                reasoning_phase, scratchpad_phase
            )
            if actionable_steps:
                output += "\n\n" + actionable_steps
        
        return output
    
    def _calculate_uncertainty(self, reasoning_phase: Any) -> float:
        """Calculate overall uncertainty from reasoning phase."""
        if not reasoning_phase or not reasoning_phase.hypotheses:
            return 0.5
        
        # Uncertainty is inverse of average confidence
        avg_confidence = sum(
            h.confidence for h in reasoning_phase.hypotheses
        ) / len(reasoning_phase.hypotheses)
        
        return 1.0 - avg_confidence
    
    def _extract_plan(self, reasoning_phase: Any,
                     scratchpad_phase: Any) -> Dict[str, Any]:
        """Extract implementation plan from phases."""
        plan = {
            "steps": [],
            "next_actions": [],
        }
        
        if reasoning_phase:
            # Next actions based on hypothesis status
            for hyp in reasoning_phase.hypotheses:
                if hyp.status.value == "active":
                    plan["next_actions"].append(
                        f"Continue testing: {hyp.statement[:50]}..."
                    )
                elif hyp.status.value == "inconclusive":
                    plan["next_actions"].append(
                        f"Gather more evidence for: {hyp.statement[:50]}..."
                    )
        
        if scratchpad_phase:
            plan["steps"].append(
                f"Evidence gathered: {len(scratchpad_phase.evidence_sources)} sources"
            )
        
        return plan
    
    def _extract_assumptions(self, structure_phase: Any) -> List[str]:
        """Extract explicit assumptions from structure phase."""
        assumptions = []
        
        if structure_phase:
            assumptions.append(
                f"Task scope: {structure_phase.task_description}"
            )
            if structure_phase.ontology.boundaries:
                for boundary in structure_phase.ontology.boundaries:
                    assumptions.append(
                        f"Boundary: {boundary.description}"
                    )
        
        return assumptions
    
    def _format_dissent(self, reasoning_phase: Any) -> str:
        """Format dissent notes from hypotheses."""
        dissent_items = []
        
        for hyp in reasoning_phase.hypotheses:
            if hyp.dissent_notes:
                dissent_items.append(
                    f"Regarding '{hyp.statement}': {hyp.dissent_notes[0]}"
                )
        
        if not dissent_items:
            return ""
        
        dissent_text = "DISSENTING VIEWPOINTS:\n\n"
        for item in dissent_items:
            dissent_text += f"• {item}\n"
        
        return dissent_text
    
    def _extract_actionable_steps(self, reasoning_phase: Any,
                                  scratchpad_phase: Any) -> str:
        """Extract actionable next steps."""
        steps = []
        
        if reasoning_phase:
            for hyp in reasoning_phase.hypotheses:
                if hyp.status.value == "active":
                    steps.append(
                        f"Test hypothesis: {hyp.statement}"
                    )
                    if hyp.tests:
                        steps.append(
                            f"  - Execute {len(hyp.tests)} falsifiable tests"
                        )
        
        if scratchpad_phase:
            steps.append(
                f"Review {len(scratchpad_phase.evidence_sources)} evidence sources"
            )
        
        if not steps:
            return ""
        
        action_text = "ACTIONABLE NEXT STEPS:\n\n"
        for i, step in enumerate(steps, 1):
            action_text += f"{i}. {step}\n"
        
        return action_text
    
    def _generate_hypothesis_summary(self, hypotheses: List[Any]) -> str:
        """Generate detailed summary of hypotheses for scientist facet."""
        if not hypotheses:
            return "No hypotheses generated."
        
        summary = f"Analysis of {len(hypotheses)} rival hypotheses:\n\n"
        
        for i, hyp in enumerate(hypotheses, 1):
            status_icon = {
                "active": "🔬",
                "supported": "✅",
                "falsified": "❌",
                "inconclusive": "❓",
                "suspended": "⏸️"
            }.get(hyp.status.value, "🔍")
            
            summary += f"{status_icon} Hypothesis {i}: {hyp.statement}\n"
            summary += f"   Rationale: {hyp.rationale}\n"
            summary += f"   Confidence: {hyp.confidence:.2f} ({'high' if hyp.confidence > 0.7 else 'moderate' if hyp.confidence > 0.4 else 'low'})\n"
            summary += f"   Status: {hyp.status.value}\n"
            
            if hyp.tests:
                passed = sum(1 for t in hyp.tests if t.result and t.result.value == "pass")
                failed = sum(1 for t in hyp.tests if t.result and t.result.value == "fail")
                summary += f"   Tests: {passed} passed, {failed} failed, {len(hyp.tests)} total\n"
            
            if hyp.dissent_notes:
                summary += f"   Dissent: {hyp.dissent_notes[0][:100]}...\n"
            
            summary += "\n"
        
        return summary
    
    def _generate_therapist_message(self, reasoning_phase: Any, 
                                   context: Dict[str, Any]) -> str:
        """Generate empathetic therapist framing."""
        message = "Navigating complex reasoning requires patience and methodical thinking. "
        
        if reasoning_phase and reasoning_phase.hypotheses:
            active_count = sum(1 for h in reasoning_phase.hypotheses 
                            if h.status.value == "active")
            falsified_count = sum(1 for h in reasoning_phase.hypotheses 
                                if h.status.value == "falsified")
            
            if falsified_count > 0:
                message += f"We've learned from {falsified_count} hypothesis{'es' if falsified_count > 1 else ''} that didn't hold up to testing. "
                message += "This is valuable - each falsification brings us closer to understanding. "
            
            if active_count > 0:
                message += f"Currently, {active_count} hypothesis{'es are' if active_count > 1 else ' is'} being actively explored. "
                message += "Let's continue gathering evidence to refine our understanding. "
        
        if context.get("uncertainty", 0) > 0.6:
            message += "It's okay to feel uncertain - this is a natural part of the reasoning process. "
            message += "We're building understanding step by step. "
        
        message += "Each piece of evidence, each test result, contributes to a clearer picture."
        
        return message
    
    def _generate_generalist_insights(self, evidence_sources: List[Any],
                                     context: Dict[str, Any]) -> str:
        """Generate cross-domain insights from evidence."""
        if not evidence_sources:
            return "No evidence gathered yet."
        
        insights = f"Drawing insights from {len(evidence_sources)} evidence source{'s' if len(evidence_sources) > 1 else ''}:\n\n"
        
        # Categorize evidence by type
        evidence_types = {}
        for evidence in evidence_sources:
            ev_type = evidence.source_type.value
            if ev_type not in evidence_types:
                evidence_types[ev_type] = []
            evidence_types[ev_type].append(evidence)
        
        for ev_type, sources in evidence_types.items():
            insights += f"• {ev_type.replace('_', ' ').title()}: {len(sources)} source{'s' if len(sources) > 1 else ''}\n"
            avg_reliability = sum(s.reliability_score for s in sources) / len(sources)
            insights += f"  Average reliability: {avg_reliability:.2f}\n"
        
        # Add analogies if provided
        if context.get("analogies"):
            insights += "\nCross-domain analogies:\n"
            for analogy in context.get("analogies", []):
                insights += f"  • {analogy.get('domain', 'Unknown')}: {analogy.get('analogy', '')}\n"
        
        return insights
    
    def _generate_engineer_insights(self, scratchpad_phase: Any,
                                   reasoning_phase: Any) -> str:
        """Generate technical implementation insights."""
        insights = "Technical Implementation Analysis:\n\n"
        
        if scratchpad_phase:
            insights += f"Evidence Sources: {len(scratchpad_phase.evidence_sources)}\n"
            insights += f"Memory Entries: {scratchpad_phase.memory_store.get_summary()['total_entries']}\n"
            
            # Analyze evidence quality
            if scratchpad_phase.evidence_sources:
                avg_reliability = sum(
                    e.reliability_score for e in scratchpad_phase.evidence_sources
                ) / len(scratchpad_phase.evidence_sources)
                insights += f"Average Evidence Reliability: {avg_reliability:.2f}\n"
        
        if reasoning_phase and reasoning_phase.hypotheses:
            insights += "\nHypothesis Testing Status:\n"
            for hyp in reasoning_phase.hypotheses:
                if hyp.tests:
                    insights += f"  • {hyp.statement[:50]}...\n"
                    insights += f"    Tests: {len(hyp.tests)} designed, "
                    executed = sum(1 for t in hyp.tests if t.result is not None)
                    insights += f"{executed} executed\n"
        
        return insights

