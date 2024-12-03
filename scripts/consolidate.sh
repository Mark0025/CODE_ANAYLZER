#!/bin/bash

# Consolidate scripts
mv start.sh scripts/
mv start-test.sh scripts/
mv setup.sh scripts/

# Create single entry point
cat > run.sh << EOL
#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Run CODE_ANALYZER CLI
python -m code_analyzer.cli.main "\$@"
EOL

chmod +x run.sh 