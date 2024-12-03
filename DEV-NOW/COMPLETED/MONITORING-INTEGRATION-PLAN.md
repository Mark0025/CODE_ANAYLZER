# Monitoring Integration Fix Plan - Part 6 🎯

## Direct File Edit Approach

### 1. First, let's find all instances:

```bash
# Search for log_data in all Python files
find code_analyzer/monitoring -name "*.py" -exec grep -l "log_data" {} \;
```

### 2. ONE Command Fix (Python):

```python
# Create fix_column.py
cat > scripts/fix_column.py << 'EOL'
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
EOL

# Run fix
python scripts/fix_column.py
```

### 3. Verification:

```bash
# 1. Check file was modified
git diff code_analyzer/monitoring/dashboard.py

# 2. Restart monitoring
pkill -f "uvicorn"
uvicorn code_analyzer.monitoring.dashboard:app --reload

# 3. Test endpoint
curl http://localhost:8000/
```

### 4. Success Metrics:
- [ ] File updated successfully
- [ ] No "no such column" errors
- [ ] Dashboard loads correctly

### 5. Rollback Plan:

```bash
git checkout -- code_analyzer/monitoring/dashboard.py
```

Following .currsorules:
- Using Python for reliability
- Clear verification
- ONE command solution
- Learning from errors