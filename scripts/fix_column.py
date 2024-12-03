from pathlib import Path

def fix_column_name():
    dashboard_path = Path("code_analyzer/monitoring/dashboard.py")
    if dashboard_path.exists():
        content = dashboard_path.read_text()
        updated = content.replace("log_data", "log_metadata")
        dashboard_path.write_text(updated)
        print("✅ Updated dashboard.py")

if __name__ == "__main__":
    fix_column_name()
