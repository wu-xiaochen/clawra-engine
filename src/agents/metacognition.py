from .base import BaseAgent
from typing import Any, Dict, List, Optional
import logging
import re

logger = logging.getLogger(__name__)

class MetacognitiveAgent(BaseAgent):
    """
    Metacognitive Agent with self-assessment capabilities
    
    Implements:
    - Confidence calibration based on evidence quality
    - Knowledge boundary detection
    - Self-reflection with reasoning validation
    """
    
    # Confidence thresholds for knowledge boundary
    CONFIDENCE_HIGH = 0.85
    CONFIDENCE_MEDIUM = 0.60
    CONFIDENCE_LOW = 0.40
    
    async def reflect(self, thought: str, reasoning_steps: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Self-reflection: Validate reasoning against ontology logic
        
        Args:
            thought: The thought or conclusion to reflect upon
            reasoning_steps: The reasoning steps that led to this thought
            
        Returns:
            Reflection result with validity assessment
        """
        logger.info(f"{self.name} reflecting on: {thought[:100]}...")
        
        reflection_result = {
            "valid": True,
            "confidence": 0.0,
            "issues": [],
            "suggestions": []
        }
        
        # Check if reasoning has sufficient evidence
        if reasoning_steps:
            total_confidence = sum(step.get("confidence", 0.5) for step in reasoning_steps)
            avg_confidence = total_confidence / len(reasoning_steps) if reasoning_steps else 0.0
            reflection_result["confidence"] = avg_confidence
            
            # Identify low confidence steps
            low_confidence_steps = [
                i for i, step in enumerate(reasoning_steps) 
                if step.get("confidence", 1.0) < self.CONFIDENCE_MEDIUM
            ]
            
            if low_confidence_steps:
                reflection_result["issues"].append(
                    f"Low confidence in reasoning steps: {low_confidence_steps}"
                )
                reflection_result["suggestions"].append(
                    "Consider gathering more evidence for uncertain conclusions"
                )
        
        
        # Validate logical consistency
        if self._detect_contradictions(thought):
            reflection_result["valid"] = False
            reflection_result["issues"].append("Potential contradiction detected in reasoning")
        
        
        return reflection_result
    
    
    def _detect_contradictions(self, text: str) -> bool:
        """
        Simple contradiction detection
        In production, this would use the reasoner for logical validation
        """
        # Simple pattern-based contradiction detection
        contradiction_patterns = [
            r'is not.*is',
            r'cannot.*can',
            r'impossible.*possible',
            r'false.*true'
        ]
        
        for pattern in contradiction_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
        
    async def run(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute task loop: Think -> Reflect -> Act -> Learn
        
        Args:
            task: The task to execute
            context: Additional context for the task
            
        Returns:
            Execution result with confidence assessment
        """
        logger.info(f"Starting metacognitive task: {task[:100]}...")
        
        # Execute forward chain reasoning
        inference = self.reasoner.forward_chain(max_depth=5)
        explanation = self.reasoner.explain(inference)
        
        # Build structured reasoning steps
        steps = []
        for step in inference.conclusions:
            steps.append({
                "rule": step.rule.name,
                "premise": f"({step.matched_facts[0].subject} → {step.matched_facts[0].predicate} → {step.matched_facts[0].object})",
                "conclusion": f"({step.conclusion.subject} → {step.conclusion.predicate} → {step.conclusion.object})",
                "confidence": round(step.confidence.value, 4)
            })
        
        # Perform self-reflection
        reflection = await self.reflect(explanation, steps)
        
        # Assess knowledge boundary
        boundary_check = self.check_knowledge_boundary(task, inference.total_confidence.value)
        
        return {
            "status": "success",
            "result": explanation,
            "inference_steps": steps,
            "facts_used_count": len(inference.facts_used),
            "total_confidence": round(inference.total_confidence.value, 4),
            "reflection": reflection,
            "knowledge_boundary": boundary_check
        }
    
    
    def check_knowledge_boundary(self, query: str, confidence: float) -> Dict[str, Any]:
        """
        Check if the query is within the knowledge boundary
        
        Args:
            query: The user's query
            confidence: Current confidence level
            
        Returns:
            Boundary assessment with recommendations
        """
        boundary_result = {
            "within_boundary": True,
            "confidence_level": "high",
            "message": "",
            "recommendation": None
        }
        
        # Determine confidence level
        if confidence >= self.CONFIDENCE_HIGH:
            boundary_result["confidence_level"] = "high"
            boundary_result["message"] = "High confidence in the reasoning result"
        elif confidence >= self.CONFIDENCE_MEDIUM:
            boundary_result["confidence_level"] = "medium"
            boundary_result["message"] = "Moderate confidence - consider verifying critical facts"
        elif confidence >= self.CONFIDENCE_LOW:
            boundary_result["confidence_level"] = "low"
            boundary_result["message"] = "Low confidence - knowledge boundary approaching"
            boundary_result["recommendation"] = "Consider consulting external sources or human expert"
        else:
            boundary_result["within_boundary"] = False
            boundary_result["confidence_level"] = "unknown"
            boundary_result["message"] = "Query appears to be outside knowledge boundary"
            boundary_result["recommendation"] = "Unable to provide reliable answer - please consult domain expert"
        
        
        return boundary_result
    
    
    def calibrate_confidence(self, evidence_count: int, evidence_quality: float = 0.8) -> float:
        """
        Calibrate confidence based on evidence quantity and quality
        
        Uses Bayesian-inspired calibration:
        - More evidence increases confidence
        - Lower quality evidence reduces confidence boost
        
        Args:
            evidence_count: Number of evidence pieces
            evidence_quality: Average quality of evidence (0-1)
            
        Returns:
            Calibrated confidence score
        """
        if evidence_count == 0:
            return 0.0
        
        # Evidence scaling: diminishing returns after 5 pieces
        evidence_factor = min(evidence_count / 5.0, 1.0)
        
        # Quality adjustment: high quality evidence boosts confidence
        quality_factor = evidence_quality
        
        # Combined confidence with base uncertainty
        base_uncertainty = 0.1  # Minimum uncertainty
        calibrated = (evidence_factor * quality_factor * (1 - base_uncertainty)) + base_uncertainty
        
        return min(calibrated, 0.99)  # Cap at 0.99 to maintain humility
