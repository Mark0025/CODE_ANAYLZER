# API Key Handling Best Practices

## Crew Implementation Pattern
1. All crews inherit from BaseCrew
2. BaseCrew handles API key loading
3. Use self.api_key consistently

## Code Pattern
```python
class BaseCrew:
    def __init__(self, name: str, target_path: str):
        # Load environment variables first
        load_dotenv()
        
        # Get and verify API key once
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")

class SpecificCrew(BaseCrew):
    def __init__(self, target_path: str):
        super().__init__("CrewName", target_path)
        
        # Use inherited API key
        self.client = OpenAI(api_key=self.api_key)
```

## Testing Pattern
1. Use conftest.py for environment setup
2. Load real API key from .env
3. No hardcoded values
4. Skip tests if no API key found

## Verification Steps
1. Run environment test:
   ```bash
   pytest tests/test_environment.py -v
   ```

2. Run real analysis:
   ```bash
   pytest tests/test_real_analysis.py -v
   ```

3. Check crew initialization:
   ```bash
   pytest tests/test_crews.py -v
   ```