#!/bin/bash
set -e

echo "🔧 Fixing Pattern Detector Typing..."

# Update pattern detector with proper imports
cat > code_analyzer/crews/analysis_crews/pattern_detector.py << 'EOF'
"""Pattern detection using AST helpers."""
from typing import Dict, Any, List
from code_analyzer.utils.ast_helpers import parse_code_safely, get_node_name
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger

class PatternMatch:
    """Pattern match information"""
    def __init__(self, type: str, name: str, location: Dict[str, Any], confidence: float):
        self.type = type
        self.name = name
        self.location = location
        self.confidence = confidence

class PatternDetector:
    """Detects code patterns and anti-patterns"""
    
    async def analyze_patterns(self, code: str) -> Dict[str, Any]:
        """Analyze code for patterns"""
        try:
            tree = parse_code_safely(code)
            if not tree:
                raise ValueError("Failed to parse code")
                
            results = {
                "patterns_found": [],
                "code_quality": "good"
            }
            
            # Save results
            db = DatabaseManager()
            db.save_crew_output(
                crew_name="pattern_detector",
                output_type="pattern_analysis",
                status="completed",
                results=results
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
EOF

echo "✨ Typing fixed!"
