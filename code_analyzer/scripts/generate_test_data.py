"""Generate comprehensive test data for all components."""
from datetime import datetime, timedelta
from code_analyzer.models.db_manager import DatabaseManager
from code_analyzer.models.development_timeline import (
    DevelopmentEvent, FileChange, ShellCommand, 
    CrewOperation, TestResult
)

def generate_complete_test_data():
    """Generate test data for all components."""
    db = DatabaseManager()
    
    # Create crews and their activities
    crews = ["AnalysisCrew", "DocumentationCrew", "TestingCrew"]
    
    for crew_name in crews:
        # 1. Create Development Event
        event = DevelopmentEvent(
            event_type="crew_operation",
            title=f"{crew_name} Development Activity",
            description=f"Test activity for {crew_name}",
            event_data={
                "start_time": datetime.utcnow().timestamp(),
                "environment": "test"
            }
        )
        
        # 2. Add File Changes
        file_change = FileChange(
            file_path=f"test/{crew_name.lower()}/test_file.py",
            change_type="modify",
            content_before="old content",
            content_after="new content",
            change_data={
                "lines_changed": 10,
                "complexity_delta": -2
            }
        )
        event.files_changed.append(file_change)
        
        # 3. Add Shell Commands
        command = ShellCommand(
            command=f"python -m {crew_name.lower()}.main",
            status=0,
            output="Success",
            command_data={
                "duration": 5.2,
                "memory_peak": "128MB"
            }
        )
        event.shell_commands.append(command)
        
        # 4. Add Crew Operation
        operation = CrewOperation(
            crew_name=crew_name,
            operation="analyze",
            status="completed",
            result={"findings": "test results"},
            operation_data={
                "duration": 10.5,
                "resources_used": ["GPU", "CPU"]
            }
        )
        event.crew_operations.append(operation)
        
        # 5. Add Test Results
        test = TestResult(
            test_name=f"{crew_name}Test",
            status="pass",
            duration=2.5,
            test_data={
                "coverage": 95,
                "assertions": 50
            }
        )
        event.test_results.append(test)
        
        # Save event and all related data
        db.session.add(event)
        
        # 6. Create Crew Output
        output = db.save_crew_output(
            crew_name=crew_name,
            output={
                "status": "completed",
                "message": f"{crew_name} operation complete",
                "start_time": datetime.utcnow().timestamp(),
                "end_time": datetime.utcnow().timestamp() + 5,
                "details": {
                    "files_processed": 10,
                    "memory_used": "128MB",
                    "cpu_usage": "45%"
                }
            }
        )
        
        # 7. Create Logs for each level
        for level in ["INFO", "DEBUG", "WARNING", "ERROR"]:
            db.save_log_entry(
                level=level,
                message=f"Test {level} message for {crew_name}",
                metadata={
                    "function": f"{crew_name.lower()}_main",
                    "file": f"{crew_name.lower()}/main.py",
                    "line": 42,
                    "thread": "MainThread",
                    "start_time": datetime.utcnow().timestamp(),
                    "end_time": datetime.utcnow().timestamp() + 1,
                    "memory_usage": 128000000
                },
                crew_name=crew_name
            )
    
    db.session.commit()
    print("Test data generated successfully!")

if __name__ == "__main__":
    generate_complete_test_data() 