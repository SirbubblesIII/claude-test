"""
Basic test to verify the module structure and imports work correctly.
"""

def test_imports():
    """Test that all modules can be imported."""
    try:
        from sage_reasoning import (
            ReasoningPipeline,
            StructurePhase,
            DSRPOntology,
            ReasoningPhase,
            Hypothesis,
            FalsifiableTest,
            ScratchpadPhase,
            EvidenceSource,
            MemoryOperation,
            PresentationPhase,
            SageVoice,
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_structure_phase():
    """Test structure phase initialization."""
    try:
        from sage_reasoning import StructurePhase
        
        phase = StructurePhase(task_description="Test task")
        phase.initialize_core_entities()
        
        assert len(phase.ontology.distinctions) > 0
        assert len(phase.ontology.systems) > 0
        assert len(phase.ontology.boundaries) > 0
        
        print("✓ Structure phase works")
        return True
    except Exception as e:
        print(f"✗ Structure phase test failed: {e}")
        return False


def test_reasoning_phase():
    """Test reasoning phase."""
    try:
        from sage_reasoning import ReasoningPhase, HypothesisStatus
        
        phase = ReasoningPhase(task_id="test")
        hypotheses = phase.generate_rival_hypotheses("Test task", min_hypotheses=2)
        
        assert len(hypotheses) >= 2
        assert all(h.status == HypothesisStatus.ACTIVE for h in hypotheses)
        
        for hyp in hypotheses:
            phase.design_tests(hyp)
            phase.specify_kill_steps(hyp)
            assert len(hyp.tests) > 0
            assert len(hyp.kill_steps) > 0
        
        print("✓ Reasoning phase works")
        return True
    except Exception as e:
        print(f"✗ Reasoning phase test failed: {e}")
        return False


def test_scratchpad_phase():
    """Test scratchpad phase."""
    try:
        from sage_reasoning import ScratchpadPhase, EvidenceSourceType
        
        phase = ScratchpadPhase(task_id="test")
        
        # Test evidence source creation
        evidence = phase.execute_tool_call(
            "test_tool",
            "test query"
        )
        
        assert evidence.source_type == EvidenceSourceType.TOOL_EXECUTION
        assert evidence.query == "test query"
        
        # Test memory operations
        memory_op = phase.decide_memory_write(
            evidence,
            "hypothesis_123",
            0.8,
            ["test", "evidence"]
        )
        
        assert memory_op.operation_type.value == "write"
        assert len(phase.memory_store.entries) > 0
        
        print("✓ Scratchpad phase works")
        return True
    except Exception as e:
        print(f"✗ Scratchpad phase test failed: {e}")
        return False


def test_presentation_phase():
    """Test presentation phase."""
    try:
        from sage_reasoning import PresentationPhase, SageVoice
        
        phase = PresentationPhase(task_id="test")
        
        assert phase.sage_voice is not None
        assert phase.preserve_dissent == True
        assert phase.include_actionable_steps == True
        
        # Test sage voice composition
        output = phase.sage_voice.compose(
            {"therapist": "Test content"},
            {"difficulty": True, "uncertainty": 0.6}
        )
        
        assert len(output) > 0
        
        print("✓ Presentation phase works")
        return True
    except Exception as e:
        print(f"✗ Presentation phase test failed: {e}")
        return False


def test_pipeline():
    """Test full pipeline."""
    try:
        from sage_reasoning import ReasoningPipeline
        
        pipeline = ReasoningPipeline()
        
        # Simple execution
        trace = pipeline.execute(
            "Test task",
            {"min_hypotheses": 2}
        )
        
        assert trace.task_description == "Test task"
        assert trace.structure_phase is not None
        assert trace.reasoning_phase is not None
        assert trace.scratchpad_phase is not None
        assert trace.presentation_phase is not None
        assert len(trace.final_output) > 0
        
        print("✓ Full pipeline works")
        return True
    except Exception as e:
        print(f"✗ Pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Running basic tests...\n")
    
    tests = [
        test_imports,
        test_structure_phase,
        test_reasoning_phase,
        test_scratchpad_phase,
        test_presentation_phase,
        test_pipeline,
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    if all(results):
        print("="*60)
        print("All tests passed! ✓")
        print("="*60)
        return 0
    else:
        print("="*60)
        print("Some tests failed ✗")
        print("="*60)
        return 1


if __name__ == "__main__":
    exit(main())

