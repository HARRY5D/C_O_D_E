"""
Advanced metrics calculations including Halstead metrics and composite indices.
"""

import math
from typing import List, Dict, Any
from collections import Counter

from .parsers.base_parser import FunctionMetrics, FileMetrics


class MetricsCalculator:
    """Advanced metrics calculator for code complexity analysis"""
    
    @staticmethod
    def calculate_halstead_metrics(operators: List[str], operands: List[str]) -> Dict[str, float]:
        """
        Calculate Halstead software metrics.
        
        Args:
            operators: List of operators found in the code
            operands: List of operands found in the code
            
        Returns:
            Dictionary containing Halstead metrics
        """
        if not operators and not operands:
            return {
                'vocabulary': 0,
                'length': 0,
                'difficulty': 0,
                'volume': 0,
                'effort': 0,
                'time': 0,
                'bugs': 0
            }
        
        # Count unique and total occurrences
        unique_operators = len(set(operators))
        unique_operands = len(set(operands))
        total_operators = len(operators)
        total_operands = len(operands)
        
        # Basic Halstead metrics
        vocabulary = unique_operators + unique_operands  # n
        length = total_operators + total_operands        # N
        
        # Avoid division by zero
        if unique_operands == 0:
            difficulty = 0
            volume = 0
        else:
            difficulty = (unique_operators / 2) * (total_operands / unique_operands)
            volume = length * math.log2(max(1, vocabulary))
        
        effort = difficulty * volume
        time = effort / 18  # Stroud number
        bugs = volume / 3000  # Halstead's delivered bugs estimation
        
        return {
            'vocabulary': vocabulary,
            'length': length,
            'difficulty': difficulty,
            'volume': volume,
            'effort': effort,
            'time': time,
            'bugs': bugs
        }
    
    @staticmethod
    def calculate_maintainability_index(loc: int, complexity: int, halstead_volume: float) -> float:
        """
        Calculate Maintainability Index (MI).
        
        MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
        
        Args:
            loc: Lines of code
            complexity: Cyclomatic complexity
            halstead_volume: Halstead volume
            
        Returns:
            Maintainability index (0-100 scale)
        """
        if loc <= 0:
            return 100.0
        
        try:
            # Use minimum values to avoid log(0)
            safe_volume = max(1, halstead_volume)
            safe_loc = max(1, loc)
            safe_complexity = max(1, complexity)
            
            mi = (171 - 5.2 * math.log(safe_volume) - 
                  0.23 * safe_complexity - 16.2 * math.log(safe_loc))
            
            # Normalize to 0-100 scale
            return max(0, min(100, mi))
        except (ValueError, OverflowError):
            return 50.0  # Default fallback value
    
    @staticmethod
    def calculate_cognitive_complexity(nesting_levels: List[int], complexity_increments: List[int]) -> int:
        """
        Calculate Cognitive Complexity (alternative to Cyclomatic Complexity).
        
        Args:
            nesting_levels: List of nesting levels for each complexity increment
            complexity_increments: List of complexity increments
            
        Returns:
            Cognitive complexity score
        """
        cognitive_complexity = 0
        
        for i, increment in enumerate(complexity_increments):
            nesting = nesting_levels[i] if i < len(nesting_levels) else 0
            # Each nesting level multiplies the increment
            cognitive_complexity += increment * max(1, nesting)
        
        return cognitive_complexity
    
    @staticmethod
    def calculate_technical_debt_ratio(maintainability_index: float, 
                                     target_mi: float = 85.0) -> float:
        """
        Calculate technical debt ratio based on maintainability index.
        
        Args:
            maintainability_index: Current MI value
            target_mi: Target MI value (ideal maintainability)
            
        Returns:
            Technical debt ratio (0.0 = no debt, 1.0 = maximum debt)
        """
        if maintainability_index >= target_mi:
            return 0.0
        
        debt_ratio = (target_mi - maintainability_index) / target_mi
        return min(1.0, max(0.0, debt_ratio))
    
    @staticmethod
    def calculate_code_quality_score(file_metrics: FileMetrics) -> Dict[str, Any]:
        """
        Calculate overall code quality score based on multiple metrics.
        
        Args:
            file_metrics: FileMetrics object containing all metrics
            
        Returns:
            Dictionary containing quality scores and recommendations
        """
        if not file_metrics.functions:
            return {
                'overall_score': 100.0,
                'complexity_score': 100.0,
                'maintainability_score': file_metrics.maintainability_index,
                'size_score': 100.0,
                'recommendations': []
            }
        
        # Calculate component scores
        complexity_score = MetricsCalculator._calculate_complexity_score(file_metrics.functions)
        size_score = MetricsCalculator._calculate_size_score(file_metrics)
        maintainability_score = file_metrics.maintainability_index
        
        # Weighted overall score
        overall_score = (
            complexity_score * 0.4 +
            maintainability_score * 0.4 +
            size_score * 0.2
        )
        
        # Generate recommendations
        recommendations = MetricsCalculator._generate_recommendations(file_metrics)
        
        return {
            'overall_score': round(overall_score, 2),
            'complexity_score': round(complexity_score, 2),
            'maintainability_score': round(maintainability_score, 2),
            'size_score': round(size_score, 2),
            'recommendations': recommendations
        }
    
    @staticmethod
    def _calculate_complexity_score(functions: List[FunctionMetrics]) -> float:
        """Calculate complexity score (0-100, higher is better)"""
        if not functions:
            return 100.0
        
        total_complexity = sum(f.cyclomatic_complexity for f in functions)
        avg_complexity = total_complexity / len(functions)
        
        # Score decreases as complexity increases
        # Good: CC <= 5, Moderate: 6-10, High: 11-20, Very High: 21+
        if avg_complexity <= 5:
            return 100.0
        elif avg_complexity <= 10:
            return 80.0 - (avg_complexity - 5) * 4  # 80 to 60
        elif avg_complexity <= 20:
            return 60.0 - (avg_complexity - 10) * 3  # 60 to 30
        else:
            return max(10.0, 30.0 - (avg_complexity - 20) * 2)
    
    @staticmethod
    def _calculate_size_score(file_metrics: FileMetrics) -> float:
        """Calculate size score based on function sizes (0-100, higher is better)"""
        if not file_metrics.functions:
            return 100.0
        
        avg_function_size = sum(f.lines_of_code for f in file_metrics.functions) / len(file_metrics.functions)
        
        # Ideal function size: 10-50 LOC
        if 10 <= avg_function_size <= 50:
            return 100.0
        elif avg_function_size < 10:
            return 80.0 + (avg_function_size * 2)  # Small penalty for very small functions
        elif avg_function_size <= 100:
            return 100.0 - (avg_function_size - 50)  # Linear decrease
        else:
            return max(10.0, 50.0 - (avg_function_size - 100) * 0.5)
    
    @staticmethod
    def _generate_recommendations(file_metrics: FileMetrics) -> List[str]:
        """Generate code improvement recommendations"""
        recommendations = []
        
        if not file_metrics.functions:
            return recommendations
        
        # Check average complexity
        avg_complexity = sum(f.cyclomatic_complexity for f in file_metrics.functions) / len(file_metrics.functions)
        if avg_complexity > 10:
            recommendations.append("Consider breaking down complex functions (average complexity > 10)")
        
        # Check for very complex functions
        complex_functions = [f for f in file_metrics.functions if f.cyclomatic_complexity > 15]
        if complex_functions:
            recommendations.append(f"Refactor highly complex functions: {', '.join(f.name for f in complex_functions)}")
        
        # Check function sizes
        large_functions = [f for f in file_metrics.functions if f.lines_of_code > 100]
        if large_functions:
            recommendations.append(f"Consider splitting large functions: {', '.join(f.name for f in large_functions)}")
        
        # Check nesting depth
        deeply_nested = [f for f in file_metrics.functions if f.nesting_depth > 4]
        if deeply_nested:
            recommendations.append(f"Reduce nesting depth in: {', '.join(f.name for f in deeply_nested)}")
        
        # Check maintainability index
        if file_metrics.maintainability_index < 50:
            recommendations.append("Overall maintainability is low - consider comprehensive refactoring")
        elif file_metrics.maintainability_index < 70:
            recommendations.append("Consider improving code maintainability")
        
        # Check for functions with too many parameters
        param_heavy = [f for f in file_metrics.functions if f.parameters > 5]
        if param_heavy:
            recommendations.append(f"Reduce parameter count in: {', '.join(f.name for f in param_heavy)}")
        
        return recommendations
