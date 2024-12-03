"""Analyze all development history and patterns."""
from pathlib import Path
import git
import json
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.models.crew_output import CrewOutput
from code_analyzer.models.log_entry import LogEntry

console = Console()

class DevelopmentAnalyzer:
    def __init__(self):
        self.db = DatabaseManager()
        self.repo = git.Repo(".")
        self.analysis = defaultdict(dict)

    def analyze_git_patterns(self):
        """Analyze git commit patterns."""
        commits = list(self.repo.iter_commits())
        
        # Analyze commit patterns
        commit_analysis = {
            "total_commits": len(commits),
            "authors": defaultdict(int),
            "file_changes": defaultdict(int),
            "commit_times": defaultdict(int),
            "commit_days": defaultdict(int)
        }

        for commit in commits:
            # Author analysis
            commit_analysis["authors"][commit.author.name] += 1
            
            # Time analysis
            dt = datetime.fromtimestamp(commit.committed_date)
            commit_analysis["commit_times"][dt.hour] += 1
            commit_analysis["commit_days"][dt.strftime("%A")] += 1
            
            # File changes
            for file in commit.stats.files:
                commit_analysis["file_changes"][file] += 1

        self.analysis["git"] = commit_analysis

    def analyze_logs(self):
        """Analyze log patterns."""
        log_dir = Path("code_analyzer/core/output/logs")
        log_analysis = {
            "total_logs": 0,
            "levels": defaultdict(int),
            "crews": defaultdict(int),
            "errors": [],
            "warnings": []
        }

        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                with open(log_file) as f:
                    for line in f:
                        log_analysis["total_logs"] += 1
                        parts = line.split("|")
                        if len(parts) >= 4:
                            level = parts[1].strip()
                            message = parts[2].strip()
                            log_analysis["levels"][level] += 1
                            
                            if "crew_name" in parts[3]:
                                crew = parts[3].split("crew_name")[1].split('"')[2]
                                log_analysis["crews"][crew] += 1
                            
                            if level == "ERROR":
                                log_analysis["errors"].append(message)
                            elif level == "WARNING":
                                log_analysis["warnings"].append(message)

        self.analysis["logs"] = log_analysis

    def analyze_crew_performance(self):
        """Analyze crew performance patterns."""
        crew_analysis = defaultdict(lambda: {
            "operations": 0,
            "success_rate": 0,
            "avg_duration": 0,
            "errors": 0,
            "warnings": 0
        })

        # Analyze crew outputs
        outputs = self.db.session.query(CrewOutput).all()
        for output in outputs:
            crew = crew_analysis[output.crew_name]
            crew["operations"] += 1
            if output.output.get("status") == "completed":
                crew["success_rate"] += 1
            if "duration" in output.output:
                crew["avg_duration"] += output.output["duration"]

        # Analyze crew logs
        logs = self.db.session.query(LogEntry).all()
        for log in logs:
            if log.crew_name:
                crew = crew_analysis[log.crew_name]
                if log.level == "ERROR":
                    crew["errors"] += 1
                elif log.level == "WARNING":
                    crew["warnings"] += 1

        # Calculate averages
        for crew in crew_analysis.values():
            if crew["operations"] > 0:
                crew["success_rate"] = (crew["success_rate"] / crew["operations"]) * 100
                crew["avg_duration"] = crew["avg_duration"] / crew["operations"]

        self.analysis["crews"] = dict(crew_analysis)

    def print_analysis(self):
        """Print analysis results."""
        # Git Analysis Table
        git_table = Table(title="Git Analysis")
        git_table.add_column("Metric")
        git_table.add_column("Value")
        
        git_analysis = self.analysis["git"]
        git_table.add_row("Total Commits", str(git_analysis["total_commits"]))
        git_table.add_row("Active Authors", str(len(git_analysis["authors"])))
        git_table.add_row("Files Changed", str(len(git_analysis["file_changes"])))
        console.print(git_table)
        
        # Log Analysis Table
        log_table = Table(title="Log Analysis")
        log_table.add_column("Metric")
        log_table.add_column("Count")
        
        log_analysis = self.analysis["logs"]
        log_table.add_row("Total Logs", str(log_analysis["total_logs"]))
        for level, count in log_analysis["levels"].items():
            log_table.add_row(f"{level} Logs", str(count))
        console.print(log_table)
        
        # Crew Performance Table
        crew_table = Table(title="Crew Performance")
        crew_table.add_column("Crew")
        crew_table.add_column("Operations")
        crew_table.add_column("Success Rate")
        crew_table.add_column("Avg Duration")
        crew_table.add_column("Errors")
        
        for crew_name, stats in self.analysis["crews"].items():
            crew_table.add_row(
                crew_name,
                str(stats["operations"]),
                f"{stats['success_rate']:.1f}%",
                f"{stats['avg_duration']:.2f}s",
                str(stats["errors"])
            )
        console.print(crew_table)

    def analyze_all(self):
        """Run complete analysis."""
        print("Analyzing git history...")
        self.analyze_git_patterns()
        
        print("Analyzing logs...")
        self.analyze_logs()
        
        print("Analyzing crew performance...")
        self.analyze_crew_performance()
        
        print("\nAnalysis Results:")
        self.print_analysis()
        
        # Save analysis to file
        with open("code_analyzer/core/output/analysis/development_analysis.json", "w") as f:
            json.dump(self.analysis, f, indent=2)

if __name__ == "__main__":
    analyzer = DevelopmentAnalyzer()
    analyzer.analyze_all() 