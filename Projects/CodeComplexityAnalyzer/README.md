# Code Complexity Analyzer

A comprehensive tool that analyzes source code and reports code complexity metrics including Cyclomatic Complexity, Lines of Code (LOC), Nesting Depth, and Maintainability Index.

## Features

- **Multiple Programming Languages**: Currently supports Python with extensible architecture for Java, C++, JavaScript
- **Comprehensive Metrics**:
  - Lines of Code (LOC)
  - Number of Functions/Methods
  - Cyclomatic Complexity
  - Nesting Depth
  - Halstead Metrics
  - Maintainability Index
- **Dual Interface**:
  - Command Line Interface (CLI)
  - Web Interface using Streamlit
- **Export Options**:
  - JSON reports
  - CSV exports
  - Detailed console output

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### CLI Usage
```bash
# Analyze a single file
python cli.py analyze path/to/file.py

# Analyze a directory
python cli.py analyze path/to/directory --recursive

# Export results to JSON
python cli.py analyze path/to/file.py --output results.json --format json

# Export results to CSV
python cli.py analyze path/to/file.py --output results.csv --format csv
```

### Web Interface
```bash
streamlit run app.py
```

## Metrics Explained

- **Lines of Code (LOC)**: Total lines excluding comments and blank lines
- **Cyclomatic Complexity**: Measures the number of linearly independent paths through code
- **Nesting Depth**: Maximum depth of nested control structures
- **Maintainability Index**: Composite metric indicating code maintainability (0-100 scale)
- **Halstead Metrics**: Software metrics based on operators and operands

## Project Structure

```
CodeComplexityAnalyzer/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── analyzer.py          # Main analysis engine
│   │   ├── metrics.py           # Metrics calculations
│   │   └── parsers/
│   │       ├── __init__.py
│   │       ├── python_parser.py # Python AST parser
│   │       └── base_parser.py   # Base parser interface
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── cli.py              # Command line interface
│   │   └── web_app.py          # Streamlit web interface
│   └── utils/
│       ├── __init__.py
│       ├── exporters.py        # Export functionality
│       └── visualizers.py      # Chart generation
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_metrics.py
│   └── sample_code/
├── requirements.txt
├── setup.py
├── cli.py                      # CLI entry point
├── app.py                      # Streamlit app entry point
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License
