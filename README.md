# Code Analyzer 🔍

An AI-powered Python tool for intelligent code analysis, project structure optimization, and automated improvements.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Features

- **🤖 AI-Powered Analysis**: Utilizes OpenAI and CrewAI for intelligent code review
- **📊 Project Structure**: Visualizes and optimizes codebase organization
- **🔄 Dependency Tracking**: Maps and analyzes project dependencies
- **🚀 Automated Improvements**: Suggests and implements code enhancements
- **🛡️ Breaking Change Detection**: Identifies potential compatibility issues
- **📝 PR Generation**: Creates detailed pull requests for suggested changes



## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- UV package manager (recommended)

### Installation

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install code-analyzer
uv pip install code-analyzer

# Or install from source
git clone https://github.com/mark0025/code_analyzer.git
cd code_analyzer
uv venv
source .venv/bin/activate  # Unix/Mac
uv pip install -e .
```

### Environment Setup
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key-here" > .env
```

### First Run
```bash
# Run analysis on your project
code_analyzer .

# Or analyze specific directory
code_analyzer ./your-directory

# Check results
ls crews/crew-output/
```

## Configuration

Create `.code_analyzer.yaml` in your project root:

    ignore_dirs:
      - venv
      - node_modules
      - __pycache__
    
    analyze_types:
      - .py
      - .js
      - .ts

## Requirements

- Python >=3.8
- OpenAI API key
- UV package manager (recommended)

## License

MIT License - see LICENSE file for details. 