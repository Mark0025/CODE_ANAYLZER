// WebSocket connection
let ws = null;
const logsTable = document.getElementById('logs-table');

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'logs') {
            updateLogs(data.data);
        }
    };

    ws.onclose = function() {
        // Reconnect after 1 second
        setTimeout(connectWebSocket, 1000);
    };
}

function updateLogs(logs) {
    if (!logsTable) return;
    
    const rows = logs.map(log => `
        <tr>
            <td>${log.timestamp}</td>
            <td><span class="badge bg-${log.level.toLowerCase()}">${log.level}</span></td>
            <td>${log.message}</td>
            <td>${log.crew_name || 'system'}</td>
        </tr>
    `).join('');
    
    logsTable.innerHTML = rows + logsTable.innerHTML;
}

// Initialize WebSocket connection
if (logsTable) {
    connectWebSocket();
} 