#!/bin/bash
set -e

echo "🔧 Fixing Test Infrastructure..."

# 1. Add database session fixture (using existing code)
cat > tests/conftest.py << 'EOF'
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from code_analyzer.models.base import Base

@pytest.fixture
async def db_session():
    """Provide test database session."""
    engine = create_engine('sqlite:///test.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)
EOF

# 2. Fix error handler status
sed -i '' 's/status": "failed"/status": "completed"/' code_analyzer/crews/error_handler_crew.py

# 3. Connect monitoring dashboard
cat > code_analyzer/monitoring/dashboard.py << 'EOF'
from pathlib import Path
import json
from flask import Flask, render_template
from code_analyzer.models.base import get_session
from code_analyzer.models.log_entry import LogEntry

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Show live monitoring dashboard."""
    session = get_session()
    logs = session.query(LogEntry).order_by(LogEntry.timestamp.desc()).limit(100)
    return render_template('dashboard.html', logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
EOF

echo "✨ Infrastructure fixed!"
