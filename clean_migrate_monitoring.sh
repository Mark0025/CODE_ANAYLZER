#!/bin/bash
set -e

echo "🧹 Starting clean migration to FastAPI..."

# 1. Create required directories
mkdir -p code_analyzer/monitoring/templates
mkdir -p code_analyzer/monitoring/static

# 2. Apply migration YAML
python -m code_analyzer.crews.dev_crews.run_updates \
    --spec yaml_tools/fixes/migrate_to_fastapi.yaml \
    --verbose

# 3. Create template file
cat > code_analyzer/monitoring/templates/dashboard.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>CODE_ANALYZER Monitor</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8">CODE_ANALYZER Monitor</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Logs Section -->
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold mb-4">Recent Logs</h2>
                <div id="logs" class="space-y-2">
                    {% for log in logs %}
                    <div class="p-2 border rounded">
                        <span class="font-mono">{{ log.timestamp }}</span>
                        <span class="ml-2">{{ log.message }}</span>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <!-- Metrics Section -->
            <div class="bg-white rounded-lg shadow p-6">
                <h2 class="text-xl font-semibold mb-4">System Metrics</h2>
                <div id="metrics" class="space-y-4">
                    <!-- Metrics will be updated via WebSocket -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // WebSocket connection
        const ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            updateDashboard(data);
        };
        
        function updateDashboard(data) {
            // Update logs
            const logsDiv = document.getElementById("logs");
            const logEntry = document.createElement("div");
            logEntry.className = "p-2 border rounded";
            logEntry.innerHTML = `
                <span class="font-mono">${data.timestamp}</span>
                <span class="ml-2">${data.message}</span>
            `;
            logsDiv.insertBefore(logEntry, logsDiv.firstChild);
        }
    </script>
</body>
</html>
EOF

# 4. Start monitoring
echo "🚀 Starting monitoring dashboard..."
uvicorn code_analyzer.monitoring.dashboard:app --reload --port 8000

echo "✨ Migration complete! Dashboard available at http://localhost:8000"
