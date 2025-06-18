"""
Test cases for metrics calculations.
"""

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.metrics import MetricsCalculator
from core.parsers.base_parser import FunctionMetrics, FileMetrics


class TestMetricsCalculator(unittest.TestCase):
    """Test cases for MetricsCalculator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = MetricsCalculator()
    
    def test_calculate_halstead_metrics(self):
        """Test Halstead metrics calculation"""
        operators = ['+', '-', '*', '/', '=', '==', 'if', 'for']
        operands = ['x', 'y', 'z', '1', '2', '10', 'result']
        
        metrics = self.calculator.calculate_halstead_metrics(operators, operands)
        
        self.assertIn('vocabulary', metrics)
        self.assertIn('length', metrics)
        self.assertIn('difficulty', metrics)
        self.assertIn('volume', metrics)
        self.assertIn('effort', metrics)
        self.assertIn('time', metrics)
        self.assertIn('bugs', metrics)
        
        # Check that values are reasonable
        self.assertGreater(metrics['vocabulary'], 0)
        self.assertGreater(metrics['length'], 0)
        self.assertGreaterEqual(metrics['difficulty'], 0)
        self.assertGreaterEqual(metrics['volume'], 0)
    
    def test_halstead_metrics_empty_input(self):
        """Test Halstead metrics with empty input"""
        metrics = self.calculator.calculate_halstead_metrics([], [])
        
        # All metrics should be 0 for empty input
        for key in ['vocabulary', 'length', 'difficulty', 'volume', 'effort', 'time', 'bugs']:
            self.assertEqual(metrics[key], 0)
    
    def test_calculate_maintainability_index(self):
        """Test Maintainability Index calculation"""
        mi = self.calculator.calculate_maintainability_index(50, 5, 100)
        
        # MI should be between 0 and 100
        self.assertGreaterEqual(mi, 0)
        self.assertLessEqual(mi, 100)
        
        # Higher complexity should result in lower MI
        mi_high_complexity = self.calculator.calculate_maintainability_index(50, 20, 100)
        self.assertLess(mi_high_complexity, mi)
        
        # Larger codebase should result in lower MI
        mi_large_code = self.calculator.calculate_maintainability_index(200, 5, 100)
        self.assertLess(mi_large_code, mi)
    
    def test_maintainability_index_edge_cases(self):
        """Test MI calculation with edge cases"""
        # Zero LOC
        mi = self.calculator.calculate_maintainability_index(0, 5, 100)
        self.assertEqual(mi, 100.0)
        
        # Very high complexity
        mi = self.calculator.calculate_maintainability_index(100, 1000, 1000)
        self.assertGreaterEqual(mi, 0)
        self.assertLessEqual(mi, 100)
    
    def test_calculate_cognitive_complexity(self):
        """Test Cognitive Complexity calculation"""
        nesting_levels = [0, 1, 2, 1, 0]
        complexity_increments = [1, 1, 1, 1, 1]
        
        cognitive = self.calculator.calculate_cognitive_complexity(nesting_levels, complexity_increments)
        
        # Should be sum of increments weighted by nesting
        expected = 1*1 + 1*1 + 1*2 + 1*1 + 1*1  # 6
        self.assertEqual(cognitive, expected)
    
    def test_calculate_technical_debt_ratio(self):
        """Test Technical Debt Ratio calculation"""
        # Perfect maintainability
        debt = self.calculator.calculate_technical_debt_ratio(85.0, 85.0)
        self.assertEqual(debt, 0.0)
        
        # Above target
        debt = self.calculator.calculate_technical_debt_ratio(90.0, 85.0)
        self.assertEqual(debt, 0.0)
        
        # Below target
        debt = self.calculator.calculate_technical_debt_ratio(70.0, 85.0)
        self.assertGreater(debt, 0.0)
        self.assertLess(debt, 1.0)
        
        # Very poor maintainability
        debt = self.calculator.calculate_technical_debt_ratio(0.0, 85.0)
        self.assertEqual(debt, 1.0)
    
    def test_calculate_code_quality_score(self):
        """Test code quality score calculation"""
        # Create sample function metrics
        functions = [
            FunctionMetrics(
                name="simple_func",
                start_line=1,
                end_line=5,
                lines_of_code=4,
                cyclomatic_complexity=2,
                nesting_depth=1,
                parameters=2
            ),
            FunctionMetrics(
                name="complex_func",
                start_line=10,
                end_line=30,
                lines_of_code=20,
                cyclomatic_complexity=8,
                nesting_depth=3,
                parameters=4
            )
        ]
        
        file_metrics = FileMetrics(
            filepath="test.py",
            total_lines=35,
            lines_of_code=24,
            blank_lines=5,
            comment_lines=6,
            functions=functions,
            classes=["TestClass"],
            maintainability_index=75.0
        )
        
        quality = self.calculator.calculate_code_quality_score(file_metrics)
        
        self.assertIn('overall_score', quality)
        self.assertIn('complexity_score', quality)
        self.assertIn('maintainability_score', quality)
        self.assertIn('size_score', quality)
        self.assertIn('recommendations', quality)
        
        # Scores should be between 0 and 100
        for score_key in ['overall_score', 'complexity_score', 'maintainability_score', 'size_score']:
            self.assertGreaterEqual(quality[score_key], 0)
            self.assertLessEqual(quality[score_key], 100)
        
        # Recommendations should be a list
        self.assertIsInstance(quality['recommendations'], list)
    
    def test_quality_score_empty_functions(self):
        """Test quality score with no functions"""
        file_metrics = FileMetrics(
            filepath="empty.py",
            total_lines=10,
            lines_of_code=5,
            blank_lines=3,
            comment_lines=2,
            functions=[],
            classes=[],
            maintainability_index=80.0
        )
        
        quality = self.calculator.calculate_code_quality_score(file_metrics)
        
        # Should handle empty functions gracefully
        self.assertEqual(quality['overall_score'], 100.0)
        self.assertEqual(quality['complexity_score'], 100.0)
        self.assertEqual(quality['maintainability_score'], 80.0)
        self.assertEqual(quality['size_score'], 100.0)
        self.assertIsInstance(quality['recommendations'], list)


class TestMetricsIntegration(unittest.TestCase):
    """Integration tests for metrics calculations"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = MetricsCalculator()
    
    def test_realistic_function_metrics(self):
        """Test with realistic function metrics"""
        # Simulate a realistic function with moderate complexity
        functions = [
            FunctionMetrics(
                name="process_data",
                start_line=1,
                end_line=25,
                lines_of_code=20,
                cyclomatic_complexity=7,
                nesting_depth=2,
                parameters=3
            ),
            FunctionMetrics(
                name="validate_input",
                start_line=30,
                end_line=40,
                lines_of_code=8,
                cyclomatic_complexity=4,
                nesting_depth=2,
                parameters=1
            ),
            FunctionMetrics(
                name="format_output",
                start_line=45,
                end_line=55,
                lines_of_code=8,
                cyclomatic_complexity=2,
                nesting_depth=1,
                parameters=2
            )
        ]
        
        file_metrics = FileMetrics(
            filepath="realistic.py",
            total_lines=60,
            lines_of_code=36,
            blank_lines=12,
            comment_lines=12,
            functions=functions,
            classes=["DataProcessor"],
            maintainability_index=68.5
        )
        
        quality = self.calculator.calculate_code_quality_score(file_metrics)
        
        # Should be in reasonable range for moderate quality code
        self.assertGreater(quality['overall_score'], 50)
        self.assertLess(quality['overall_score'], 90)
        
        # Should have some recommendations for improvement
        self.assertGreater(len(quality['recommendations']), 0)
    
    def test_high_quality_code_metrics(self):
        """Test with high quality code metrics"""
        functions = [
            FunctionMetrics(
                name="simple_add",
                start_line=1,
                end_line=3,
                lines_of_code=2,
                cyclomatic_complexity=1,
                nesting_depth=0,
                parameters=2
            ),
            FunctionMetrics(
                name="simple_multiply",
                start_line=5,
                end_line=7,
                lines_of_code=2,
                cyclomatic_complexity=1,
                nesting_depth=0,
                parameters=2
            )
        ]
        
        file_metrics = FileMetrics(
            filepath="high_quality.py",
            total_lines=10,
            lines_of_code=4,
            blank_lines=3,
            comment_lines=3,
            functions=functions,
            classes=[],
            maintainability_index=95.0
        )
        
        quality = self.calculator.calculate_code_quality_score(file_metrics)
        
        # Should have high scores
        self.assertGreater(quality['overall_score'], 85)
        self.assertGreater(quality['complexity_score'], 90)
        self.assertGreater(quality['maintainability_score'], 90)
        
        # Should have minimal recommendations
        self.assertLessEqual(len(quality['recommendations']), 2)
    
    def test_poor_quality_code_metrics(self):
        """Test with poor quality code metrics"""
        functions = [
            FunctionMetrics(
                name="massive_function",
                start_line=1,
                end_line=150,
                lines_of_code=140,
                cyclomatic_complexity=25,
                nesting_depth=6,
                parameters=8
            )
        ]
        
        file_metrics = FileMetrics(
            filepath="poor_quality.py",
            total_lines=160,
            lines_of_code=145,
            blank_lines=10,
            comment_lines=5,
            functions=functions,
            classes=[],
            maintainability_index=25.0
        )
        
        quality = self.calculator.calculate_code_quality_score(file_metrics)
        
        # Should have low scores
        self.assertLess(quality['overall_score'], 50)
        self.assertLess(quality['complexity_score'], 30)
        self.assertLess(quality['maintainability_score'], 30)
        
        # Should have many recommendations
        self.assertGreater(len(quality['recommendations']), 3)


if __name__ == '__main__':
    unittest.main()
