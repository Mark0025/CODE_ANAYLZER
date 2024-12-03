#!/bin/bash
set -e

echo "📊 Creating Report Generation System..."

# Create report generator
cat > code_analyzer/crews/report_crews/report_generator.py << 'EOF'
"""Report generation for code analysis results."""
from typing import Dict, Any, List
from code_analyzer.models.db_manager import DatabaseManager
from loguru import logger
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pendulum
import json
from pathlib import Path

class ReportGenerator:
    """Generates analysis reports from database."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.console = Console()
        self.output_dir = Path("code_analyzer/core/output/reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def generate_report(self, analysis_id: int = None) -> Dict[str, Any]:
        """Generate comprehensive report."""
        try:
            # Get analysis results
            if analysis_id:
                results = self.db.get_crew_output(analysis_id)
            else:
                results = self.db.get_latest_crew_output("pattern_detector")
                
            if not results:
                raise ValueError("No analysis results found")
                
            # Generate report
            report = {
                "timestamp": pendulum.now().isoformat(),
                "analysis_id": analysis_id or "latest",
                "summary": self._generate_summary(results),
                "patterns": self._analyze_patterns(results),
                "metrics": self._calculate_metrics(results),
                "recommendations": self._generate_recommendations(results)
            }
            
            # Save report
            report_file = self.output_dir / f"report_{pendulum.now().strftime('%Y%m%d_%H%M%S')}.json"
            report_file.write_text(json.dumps(report, indent=2))
            
            # Create latest symlink
            latest_link = self.output_dir / "latest_report.json"
            if latest_link.exists():
                latest_link.unlink()
            latest_link.symlink_to(report_file.name)
            
            # Display report
            self._display_report(report)
            
            return report
            
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            return {"status": "failed", "error": str(e)}
            
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary."""
        return {
            "total_patterns": len(results.get("patterns_found", [])),
            "code_smells": len(results.get("code_smells", [])),
            "design_patterns": len(results.get("design_patterns", [])),
            "anti_patterns": len(results.get("anti_patterns", [])),
            "overall_quality": self._calculate_quality_score(results)
        }
        
    def _analyze_patterns(self, results: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Analyze detected patterns."""
        return {
            "code_smells": results.get("code_smells", []),
            "design_patterns": results.get("design_patterns", []),
            "anti_patterns": results.get("anti_patterns", [])
        }
        
    def _calculate_metrics(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate code metrics."""
        metrics = results.get("metrics", {})
        return {
            "class_count": metrics.get("class_count", 0),
            "method_count": metrics.get("method_count", 0),
            "complexity_score": metrics.get("complexity_score", 0),
            "quality_score": self._calculate_quality_score(results)
        }
        
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        # Add recommendations based on patterns
        for smell in results.get("code_smells", []):
            recommendations.append(smell.get("suggestion", ""))
            
        return [r for r in recommendations if r]
        
    def _calculate_quality_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall code quality score."""
        metrics = results.get("metrics", {})
        
        # Basic scoring
        score = 100.0
        
        # Deduct for code smells
        score -= len(results.get("code_smells", [])) * 5
        
        # Deduct for anti-patterns
        score -= len(results.get("anti_patterns", [])) * 10
        
        # Add for design patterns
        score += len(results.get("design_patterns", [])) * 3
        
        return max(0, min(100, score))
        
    def _display_report(self, report: Dict[str, Any]) -> None:
        """Display beautiful report."""
        # Create summary panel
        summary = Panel(
            f"""[bold green]Code Analysis Report[/]
            
Analysis ID: {report['analysis_id']}
Timestamp: {report['timestamp']}
Quality Score: {report['metrics']['quality_score']:.1f}/100
            """,
            title="Summary",
            border_style="green"
        )
        self.console.print(summary)
        
        # Show patterns table
        table = Table(title="Detected Patterns")
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right")
        table.add_column("Impact", style="yellow")
        
        patterns = report["patterns"]
        table.add_row(
            "Code Smells",
            str(len(patterns["code_smells"])),
            "Medium"
        )
        table.add_row(
            "Design Patterns",
            str(len(patterns["design_patterns"])),
            "Positive"
        )
        table.add_row(
            "Anti-Patterns",
            str(len(patterns["anti_patterns"])),
            "High"
        )
        
        self.console.print(table)
        
        # Show recommendations
        if report["recommendations"]:
            rec_panel = Panel(
                "\n".join(f"• {rec}" for rec in report["recommendations"]),
                title="Recommendations",
                border_style="yellow"
            )
            self.console.print(rec_panel)
EOF

echo "✨ Report generation system created!"
