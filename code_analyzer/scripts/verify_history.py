"""Verify history population."""
from code_analyzer.models.base import get_session
from code_analyzer.models.development_history import (
    DevelopmentEvent, FileChange, CursorConversation, DocumentationChange
)

def verify_history():
    """Verify history data."""
    session = get_session()
    try:
        # Check events
        events = session.query(DevelopmentEvent).all()
        print(f"\nFound {len(events)} development events")
        
        # Check file changes
        changes = session.query(FileChange).all()
        print(f"Found {len(changes)} file changes")
        
        # Check documentation
        docs = session.query(DocumentationChange).all()
        print(f"Found {len(docs)} documentation changes")
        
        # Print sample event
        if events:
            event = events[0]
            print("\nSample Event:")
            print(f"Title: {event.title}")
            print(f"Type: {event.event_type}")
            print(f"Files Changed: {len(event.files_changed)}")
            print(f"Documentation: {len(event.documentation)}")
            
            if event.files_changed:
                print("\nSample File Change:")
                change = event.files_changed[0]
                print(f"File: {change.file_path}")
                print(f"Type: {change.change_type}")
                
            if event.documentation:
                print("\nSample Documentation:")
                doc = event.documentation[0]
                print(f"Path: {doc.doc_path}")
                print(f"Size: {len(doc.content)} bytes")
        
    finally:
        session.close()

if __name__ == "__main__":
    verify_history() 