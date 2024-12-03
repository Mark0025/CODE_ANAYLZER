#!/usr/bin/env python3
"""
IMPORTANT: DO NOT MODIFY WITHOUT PERMISSION
Contact: THE AI RE INVESTOR (405-963-2596)
"""
from pathlib import Path
from loguru import logger
from code_analyzer.models.base import get_session
from code_analyzer.models.crew_output import LogEntry
import json
import pendulum
import re

def migrate_logs():
    """Migrate existing log files to database."""
    session = get_session()
    log_dirs = [
        Path("crews/crew-output/logs"),
        Path("tests/Logs"),
        Path("DEV-MAN-CREW/Logs")
    ]
    
    total_migrated = 0
    
    try:
        for log_dir in log_dirs:
            if not log_dir.exists():
                continue
                
            for log_file in log_dir.glob("*.log"):
                logger.info(f"Processing {log_file}")
                
                with open(log_file) as f:
                    for line in f:
                        # Parse log line
                        if match := re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \| (\w+)\s+\| (.+)', line):
                            timestamp, level, message = match.groups()
                            
                            # Create log entry
                            entry = LogEntry(
                                timestamp=pendulum.parse(timestamp),
                                level=level,
                                message=message,
                                crew_name=extract_crew_name(message),
                                log_metadata={
                                    "source_file": str(log_file),
                                    "migrated_at": pendulum.now().isoformat()
                                }
                            )
                            session.add(entry)
                            total_migrated += 1
                            
                # Commit after each file
                session.commit()
                logger.info(f"Migrated logs from {log_file}")
                
        logger.success(f"Total logs migrated: {total_migrated}")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        session.rollback()
    finally:
        session.close()

def extract_crew_name(message: str) -> str:
    """Extract crew name from log message."""
    crew_patterns = [
        r'(\w+Crew)',
        r'crew (\w+)',
        r'(\w+) crew'
    ]
    
    for pattern in crew_patterns:
        if match := re.search(pattern, message, re.IGNORECASE):
            return match.group(1)
    return "unknown"

if __name__ == "__main__":
    migrate_logs() 