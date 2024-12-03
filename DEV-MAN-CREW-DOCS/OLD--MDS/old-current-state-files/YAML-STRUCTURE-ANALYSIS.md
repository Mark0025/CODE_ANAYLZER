# CODE_ANALYZER YAML Structure Analysis 🔍

## Error vs Working Template:

```mermaid
graph TD
    A[Error] -->|Missing| B[update_plan wrapper]
    
    C[Working Template] -->|Has| D[update_plan: {...}]
    C -->|Example| E[yaml_tools/setup/restructure.yaml]
    
    F[Our YAML] -->|Wrong| G[name: ...]
    F -->|Should Be| H[update_plan: {name: ...}]
```

## Working Template Structure:

```yaml
# ✅ Working Structure (from restructure.yaml)
update_plan:            # <-- We missed this wrapper!
  name: "..."
  description: "..."
  priority: "..."
  
  phases:
    1_fix_imports:
      description: "..."
      changes:
        - type: "..."
```

## Our Current Structure:

```yaml
# ❌ Our Current Structure
name: "..."            # <-- Direct properties, no wrapper
description: "..."
priority: "..."

phases:
  1_fix_imports:
    description: "..."
```

## Fixed YAML:

```bash
# Create properly structured YAML
cat > yaml_tools/fixes/fix_imports.yaml << 'EOL'
update_plan:           # <-- Add the wrapper
  name: "Fix Import Paths"
  description: "Fix model import paths to use correct location"
  priority: "CRITICAL"

  phases:
    1_fix_imports:
      description: "Update import statements to use correct paths"
      changes:
        - type: "modify_file"
          target: "code_analyzer/cli/commands/db.py"
          updates:
            - type: "replace"
              old: "from code_analyzer.crews.models.base import init_db"
              new: "from code_analyzer.models.base import init_db"
EOL
```

## What's Working/Not:

```python
status = {
    "working": {
        "pattern_detection": "✅ Complete",
        "database": "✅ Complete",
        "yaml_tools": "✅ Available"
    },
    "not_working": {
        "yaml_structure": "❌ Missing update_plan wrapper",
        "imports": "❌ Still using wrong path"
    },
    "next_step": "Fix YAML structure using working template"
}
```

## Next Steps:
1. **Fix YAML Structure**:
   ```bash
   # Create properly structured YAML
   ./fix_yaml_structure.sh
   ```

2. **Run Update**:
   ```bash
   python -m code_analyzer.crews.dev_crews.run_updates \
       --spec yaml_tools/fixes/fix_imports.yaml \
       --verbose \
       --target ./
   ```

Would you like me to:
1. Create the fixed YAML?
2. Show more working examples?
3. Explain the structure?

This follows .currsorules by:
- Using existing tools
- Following working examples
- DRY principle
- Learning from working code