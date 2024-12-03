"""Collect all development history from existing sources."""
import os
from pathlib import Path
import git
from datetime import datetime
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.models.development_timeline import (
    DevelopmentEvent, FileChange, ShellCommand, 
    CrewOperation, TestResult
)
import json
from code_analyzer.models.crew_output import CrewOutput
from code_analyzer.models.log_entry import LogEntry

class HistoryCollector:
    def __init__(self):
        self.db = DatabaseManager()
        self.repo = git.Repo(".")
        self.root_dir = Path(".")

    def collect_git_history(self):
        """Collect all git history."""
        for commit in self.repo.iter_commits():
            # Create development event for each commit
            event = DevelopmentEvent(
                event_type="commit",
                title=commit.message.split('\n')[0],
                description=commit.message,
                timestamp=datetime.fromtimestamp(commit.committed_date),
                event_data={
                    "author": commit.author.name,
                    "hash": commit.hexsha,
                    "branch": self.repo.active_branch.name
                }
            )

            # Track file changes
            for file_path, stats in commit.stats.files.items():
                file_change = FileChange(
                    file_path=file_path,
                    change_type="modify",
                    change_data=stats
                )
                event.files_changed.append(file_change)

            self.db.session.add(event)

    def collect_log_history(self):
        """Collect all existing logs."""
        log_dir = Path("code_analyzer/core/output/logs")
        if log_dir.exists():
            for log_file in log_dir.glob("*.log"):
                with open(log_file) as f:
                    for line in f:
                        # Parse log line and create event
                        try:
                            # Basic parsing - enhance based on your log format
                            parts = line.split("|")
                            if len(parts) >= 4:
                                timestamp = parts[0].strip()
                                level = parts[1].strip()
                                message = parts[2].strip()
                                metadata = parts[3].strip()

                                event = DevelopmentEvent(
                                    event_type="log",
                                    title=f"Log Entry: {level}",
                                    description=message,
                                    timestamp=datetime.fromisoformat(timestamp),
                                    event_data={"metadata": metadata}
                                )
                                self.db.session.add(event)
                        except Exception as e:
                            print(f"Error parsing log line: {e}")

    def collect_crew_history(self):
        """Collect crew operation history."""
        crew_output_dir = Path("code_analyzer/core/output/crew-output")
        if crew_output_dir.exists():
            for output_file in crew_output_dir.glob("*.json"):
                try:
                    with open(output_file) as f:
                        data = json.load(f)
                        event = DevelopmentEvent(
                            event_type="crew_operation",
                            title=f"Crew Operation: {data.get('crew_name')}",
                            description=data.get('message', ''),
                            timestamp=datetime.fromisoformat(data.get('timestamp')),
                            event_data=data
                        )
                        
                        operation = CrewOperation(
                            crew_name=data.get('crew_name'),
                            operation=data.get('operation'),
                            status=data.get('status'),
                            result=data.get('result'),
                            operation_data=data.get('details')
                        )
                        event.crew_operations.append(operation)
                        
                        self.db.session.add(event)
                except Exception as e:
                    print(f"Error processing crew output file {output_file}: {e}")

    def collect_test_history(self):
        """Collect test execution history."""
        test_output_dir = Path("code_analyzer/core/output/test-results")
        if test_output_dir.exists():
            for result_file in test_output_dir.glob("*.json"):
                try:
                    with open(result_file) as f:
                        data = json.load(f)
                        event = DevelopmentEvent(
                            event_type="test_run",
                            title=f"Test Run: {data.get('test_suite')}",
                            description=data.get('summary', ''),
                            timestamp=datetime.fromisoformat(data.get('timestamp')),
                            event_data=data
                        )
                        
                        for test_data in data.get('tests', []):
                            test = TestResult(
                                test_name=test_data.get('name'),
                                status=test_data.get('status'),
                                duration=test_data.get('duration'),
                                error_message=test_data.get('error'),
                                test_data=test_data
                            )
                            event.test_results.append(test)
                        
                        self.db.session.add(event)
                except Exception as e:
                    print(f"Error processing test result file {result_file}: {e}")

    def collect_all(self):
        """Collect all history."""
        try:
            print("Collecting git history...")
            self.collect_git_history()
            
            print("Collecting log history...")
            self.collect_log_history()
            
            print("Collecting crew history...")
            self.collect_crew_history()
            
            print("Collecting test history...")
            self.collect_test_history()
            
            self.db.session.commit()
            print("History collection complete!")
            
        except Exception as e:
            print(f"Error collecting history: {e}")
            self.db.session.rollback()
        finally:
            self.db.session.close()

if __name__ == "__main__":
    collector = HistoryCollector()
    collector.collect_all() 