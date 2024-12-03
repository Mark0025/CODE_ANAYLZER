"""Populate development history from existing files."""
from pathlib import Path
from datetime import datetime
import git
from code_analyzer.models.development_history import (
    DevelopmentEvent, FileChange, CursorConversation, DocumentationChange
)
from code_analyzer.models.base import get_session

def populate_history():
    """Populate development history from files."""
    session = get_session()
    repo = git.Repo(".")
    
    try:
        # Process git history
        for commit in repo.iter_commits():
            # Create event for commit
            event = DevelopmentEvent(
                timestamp=datetime.fromtimestamp(commit.committed_date),
                event_type="commit",
                title=commit.message.split('\n')[0],
                description=commit.message,
                event_data={
                    "author": commit.author.name,
                    "hash": commit.hexsha
                }
            )
            session.add(event)
            
            # Track file changes
            for file in commit.stats.files:
                change = FileChange(
                    event=event,
                    file_path=file,
                    change_type="modify",
                    change_data=commit.stats.files[file]
                )
                session.add(change)
        
        # Process documentation
        doc_dirs = [
            Path("DEV-MAN-CREW-DOCS"),
            Path("DEV-NOW")
        ]
        
        for doc_dir in doc_dirs:
            for doc_file in doc_dir.rglob("*.md"):
                doc_change = DocumentationChange(
                    event=event,
                    doc_path=str(doc_file),
                    content=doc_file.read_text(),
                    doc_data={
                        "type": "markdown",
                        "size": doc_file.stat().st_size
                    }
                )
                session.add(doc_change)
        
        session.commit()
        print("History populated successfully!")
        
    except Exception as e:
        print(f"Error populating history: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_history() 