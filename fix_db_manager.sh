#!/bin/bash
set -e

echo "🔧 Adding Database Manager Methods..."

# Add required methods to DatabaseManager
cat >> code_analyzer/models/db_manager.py << 'EOF'

    def get_tables(self) -> List[str]:
        """Get all tables in database."""
        try:
            inspector = inspect(self.session.get_bind())
            return inspector.get_table_names()
        except Exception as e:
            logger.error(f"Failed to get tables: {e}")
            return []

    def get_indexes(self) -> Dict[str, List[str]]:
        """Get all indexes in database."""
        try:
            inspector = inspect(self.session.get_bind())
            indexes = {}
            for table in self.get_tables():
                indexes[table] = [idx['name'] for idx in inspector.get_indexes(table)]
            return indexes
        except Exception as e:
            logger.error(f"Failed to get indexes: {e}")
            return {}

    def verify_setup(self) -> Dict[str, bool]:
        """Verify database setup."""
        try:
            tables = self.get_tables()
            required_tables = {
                'crew_outputs': False,
                'error_handling_results': False,
                'code_analysis_results': False,
                'log_entries': False
            }
            
            for table in tables:
                if table in required_tables:
                    required_tables[table] = True
                    
            return required_tables
        except Exception as e:
            logger.error(f"Failed to verify setup: {e}")
            return {}

    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            self.session.execute(text('SELECT 1'))
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

EOF

# Update imports at top of file
sed -i '' '1i\
from sqlalchemy import inspect, text\
from typing import List, Dict\
' code_analyzer/models/db_manager.py

echo "✨ Database manager updated!"
