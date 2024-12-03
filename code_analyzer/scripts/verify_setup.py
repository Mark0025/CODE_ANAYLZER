"""Verify all components are working."""
import requests
import time
from rich.console import Console
from rich.table import Table

console = Console()

def verify_endpoints():
    """Verify all endpoints are responding."""
    base_url = "http://localhost:8000"
    endpoints = {
        "/": "Home page",
        "/dashboard": "System dashboard",
        "/crews": "Crews status",
        "/analytics": "Analytics page",
        "/codebase-overview": "Codebase overview",
        "/DEV-NOW": "Development status",
        "/api/system-status": "System status API",
        "/api/health": "Health check API",
        "/api/system-check": "System check API"
    }
    
    table = Table(title="Endpoint Status")
    table.add_column("Endpoint")
    table.add_column("Status")
    table.add_column("Response Time")
    
    for endpoint, description in endpoints.items():
        try:
            start = time.time()
            response = requests.get(f"{base_url}{endpoint}")
            duration = time.time() - start
            
            status = "✅" if response.status_code == 200 else "❌"
            table.add_row(
                endpoint,
                status,
                f"{duration:.2f}s"
            )
        except Exception as e:
            table.add_row(endpoint, "❌", f"Error: {str(e)}")
    
    console.print(table)

if __name__ == "__main__":
    verify_endpoints() 