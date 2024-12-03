"""Collect complete application history."""
import git
from pathlib import Path
import json
from datetime import datetime
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.models.development_timeline import DevelopmentEvent
from loguru import logger

class AppHistoryCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.repo = git.Repo(".")
        self.history = []

    def collect_git_history(self):
        """Collect all git commits."""
        logger.info("Collecting git history...")
        for commit in self.repo.iter_commits():
            self.history.append({
                "type": "git",
                "timestamp": datetime.fromtimestamp(commit.committed_date),
                "title": commit.message.split('\n')[0],
                "description": commit.message,
                "author": commit.author.name,
                "files": list(commit.stats.files.keys()),
                "hash": commit.hexsha
            })

    def collect_log_history(self):
        """Collect all application logs."""
        logger.info("Collecting application logs...")
        log_dir = Path("code_analyzer/core/output/logs")
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                with open(log_file) as f:
                    for line in f:
                        try:
                            parts = line.split("|")
                            if len(parts) >= 4:
                                self.history.append({
                                    "type": "log",
                                    "timestamp": datetime.fromisoformat(parts[0].strip()),
                                    "level": parts[1].strip(),
                                    "message": parts[2].strip(),
                                    "metadata": parts[3].strip()
                                })
                        except Exception as e:
                            logger.error(f"Error parsing log line: {e}")

    def collect_crew_history(self):
        """Collect all crew operations."""
        logger.info("Collecting crew history...")
        crew_outputs = self.db.session.query(CrewOutput).all()
        for output in crew_outputs:
            self.history.append({
                "type": "crew",
                "timestamp": output.timestamp,
                "crew_name": output.crew_name,
                "status": output.output.get("status"),
                "message": output.output.get("message"),
                "details": output.output.get("details", {})
            })

    def collect_development_events(self):
        """Collect all development events."""
        logger.info("Collecting development events...")
        events = self.db.session.query(DevelopmentEvent).all()
        for event in events:
            self.history.append({
                "type": "development",
                "timestamp": event.timestamp,
                "event_type": event.event_type,
                "title": event.title,
                "description": event.description,
                "data": event.event_data
            })

    def save_history(self):
        """Save collected history."""
        # Sort by timestamp
        self.history.sort(key=lambda x: x["timestamp"], reverse=True)
        
        # Save to file
        output_dir = Path("code_analyzer/core/output/history")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"app_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump({
                "collected_at": datetime.now().isoformat(),
                "total_events": len(self.history),
                "events": self.history
            }, f, indent=2, default=str)
        
        logger.info(f"History saved to {output_file}")

    def collect_all(self):
        """Collect all history."""
        try:
            self.collect_git_history()
            self.collect_log_history()
            self.collect_crew_history()
            self.collect_development_events()
            self.save_history()
            
            # Print summary
            event_types = {}
            for event in self.history:
                event_types[event["type"]] = event_types.get(event["type"], 0) + 1
            
            print("\nHistory Collection Summary:")
            print("-" * 30)
            for event_type, count in event_types.items():
                print(f"{event_type.title()}: {count} events")
            print("-" * 30)
            print(f"Total Events: {len(self.history)}")
            
        except Exception as e:
            logger.error(f"Error collecting history: {e}")
            raise

if __name__ == "__main__":
    collector = AppHistoryCollector()
    collector.collect_all() 