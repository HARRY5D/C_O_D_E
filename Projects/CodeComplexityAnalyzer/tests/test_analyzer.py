"""
Test cases for the main analyzer functionality.
"""

import unittest
import tempfile
import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.analyzer import CodeComplexityAnalyzer


class TestCodeComplexityAnalyzer(unittest.TestCase):
    """Test cases for CodeComplexityAnalyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = CodeComplexityAnalyzer()
        
        # Sample Python code for testing
        self.sample_code = '''
def simple_function():
    """A simple function with low complexity."""
    return "Hello, World!"

def complex_function(x, y, z):
    """A more complex function for testing."""
    result = 0
    
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                if y > 10:
                    result += i * z
                else:
                    result += i
            else:
                if z < 5:
                    result -= i
                else:
                    result += i // 2
    elif x < 0:
        while y > 0:
            result += y
            y -= 1
    else:
        try:
            result = z / y
        except ZeroDivisionError:
            result = 0
    
    return result

class TestClass:
    """A test class."""
    
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def process_data(self, data):
        """Method with moderate complexity."""
        processed = []
        
        for item in data:
            if isinstance(item, str):
                if len(item) > 5:
                    processed.append(item.upper())
                else:
                    processed.append(item.lower())
            elif isinstance(item, int):
                if item > 0:
                    processed.append(item * 2)
                else:
                    processed.append(0)
        
        return processed
'''
        
        # Create temporary file with sample code
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        self.temp_file.write(self.sample_code)
        self.temp_file.close()
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_analyze_file(self):
        """Test analyzing a single file"""
        result = self.analyzer.analyze_file(self.temp_file.name)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result.functions), 4)  # 4 functions in sample code
        self.assertEqual(len(result.classes), 1)    # 1 class in sample code
        self.assertGreater(result.lines_of_code, 0)
        self.assertGreater(result.maintainability_index, 0)
        self.assertLessEqual(result.maintainability_index, 100)
    
    def test_function_metrics(self):
        """Test function-level metrics"""
        result = self.analyzer.analyze_file(self.temp_file.name)
        
        # Find the complex function
        complex_func = None
        simple_func = None
        
        for func in result.functions:
            if func.name == 'complex_function':
                complex_func = func
            elif func.name == 'simple_function':
                simple_func = func
        
        self.assertIsNotNone(complex_func)
        self.assertIsNotNone(simple_func)
        
        # Complex function should have higher complexity
        self.assertGreater(complex_func.cyclomatic_complexity, simple_func.cyclomatic_complexity)
        self.assertGreater(complex_func.nesting_depth, simple_func.nesting_depth)
        self.assertEqual(complex_func.parameters, 3)
        self.assertEqual(simple_func.parameters, 0)
    
    def test_analyze_nonexistent_file(self):
        """Test analyzing a file that doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            self.analyzer.analyze_file('nonexistent_file.py')
    
    def test_analyze_invalid_python_file(self):
        """Test analyzing a file with invalid Python syntax"""
        # Create file with invalid syntax
        invalid_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
        invalid_file.write('def invalid_syntax(\n    missing closing parenthesis')
        invalid_file.close()
        
        try:
            result = self.analyzer.analyze_file(invalid_file.name)
            self.assertIsNone(result)  # Should return None for invalid files
        finally:
            os.unlink(invalid_file.name)
    
    def test_generate_summary_report(self):
        """Test generating summary report"""
        result = self.analyzer.analyze_file(self.temp_file.name)
        summary = self.analyzer.generate_summary_report([result])
        
        self.assertEqual(summary['total_files'], 1)
        self.assertEqual(summary['total_functions'], 4)
        self.assertEqual(summary['total_classes'], 1)
        self.assertGreater(summary['total_loc'], 0)
        self.assertGreater(summary['average_complexity'], 0)
        self.assertIn(summary['quality_assessment'], 
                     ['Excellent', 'Good', 'Fair', 'Needs Improvement'])
        self.assertIn('complexity_distribution', summary)
    
    def test_empty_summary_report(self):
        """Test generating summary report with no files"""
        summary = self.analyzer.generate_summary_report([])
        
        self.assertEqual(summary['total_files'], 0)
        self.assertEqual(summary['total_functions'], 0)
        self.assertEqual(summary['total_classes'], 0)
        self.assertEqual(summary['total_loc'], 0)
        self.assertEqual(summary['average_complexity'], 0)


class TestAnalyzerIntegration(unittest.TestCase):
    """Integration tests for the analyzer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = CodeComplexityAnalyzer()
        
        # Create a temporary directory with multiple Python files
        self.temp_dir = tempfile.mkdtemp()
        
        # File 1: Simple file
        with open(os.path.join(self.temp_dir, 'simple.py'), 'w') as f:
            f.write('''
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
''')
        
        # File 2: Complex file
        with open(os.path.join(self.temp_dir, 'complex.py'), 'w') as f:
            f.write('''
def very_complex_function(data, threshold, mode):
    """A function with high complexity."""
    result = []
    
    for item in data:
        if isinstance(item, dict):
            if 'value' in item:
                if item['value'] > threshold:
                    if mode == 'strict':
                        if item['value'] > threshold * 2:
                            result.append(item['value'] * 3)
                        else:
                            result.append(item['value'] * 2)
                    else:
                        result.append(item['value'])
                else:
                    if mode == 'lenient':
                        result.append(item['value'] / 2)
                    else:
                        continue
            else:
                if mode == 'default':
                    result.append(0)
        elif isinstance(item, list):
            for sub_item in item:
                if sub_item > 0:
                    result.append(sub_item)
        
    return result
''')
        
        # File 3: Non-Python file (should be ignored)
        with open(os.path.join(self.temp_dir, 'readme.txt'), 'w') as f:
            f.write('This is not a Python file.')
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_analyze_directory(self):
        """Test analyzing a directory"""
        results = self.analyzer.analyze_directory(self.temp_dir)
        
        # Should find 2 Python files
        self.assertEqual(len(results), 2)
        
        # Check that both files were analyzed
        filenames = [os.path.basename(r.filepath) for r in results]
        self.assertIn('simple.py', filenames)
        self.assertIn('complex.py', filenames)
    
    def test_analyze_directory_recursive(self):
        """Test recursive directory analysis"""
        # Create subdirectory with another Python file
        subdir = os.path.join(self.temp_dir, 'subdir')
        os.makedirs(subdir)
        
        with open(os.path.join(subdir, 'nested.py'), 'w') as f:
            f.write('def nested_function(): pass')
        
        # Analyze with recursion
        results = self.analyzer.analyze_directory(self.temp_dir, recursive=True)
        self.assertEqual(len(results), 3)  # Should find all 3 Python files
        
        # Analyze without recursion
        results = self.analyzer.analyze_directory(self.temp_dir, recursive=False)
        self.assertEqual(len(results), 2)  # Should find only 2 files in root


if __name__ == '__main__':
    unittest.main()
