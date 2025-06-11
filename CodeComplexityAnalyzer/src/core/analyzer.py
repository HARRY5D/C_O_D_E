"""
Main analyzer engine that coordinates parsing and metrics calculation.
"""

import os
import glob
from typing import List, Dict, Any, Optional
from pathlib import Path

from .parsers.base_parser import BaseParser, FileMetrics
from .parsers.python_parser import PythonParser
from .metrics import MetricsCalculator


class CodeComplexityAnalyzer:
    """Main analyzer class that orchestrates the analysis process"""
    
    def __init__(self):
        self.parsers = [
            PythonParser(),
            # Add more parsers here for other languages
        ]
        self.metrics_calculator = MetricsCalculator()
    
    def analyze_file(self, filepath: str) -> Optional[FileMetrics]:
        """
        Analyze a single file and return its metrics.
        
        Args:
            filepath: Path to the file to analyze
            
        Returns:
            FileMetrics object or None if file cannot be parsed
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Find appropriate parser
        parser = self._get_parser_for_file(filepath)
        if not parser:
            return None
        
        try:
            return parser.parse_file(filepath)
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
            return None
    
    def analyze_directory(self, directory_path: str, recursive: bool = True, 
                         file_patterns: List[str] = None) -> List[FileMetrics]:
        """
        Analyze all supported files in a directory.
        
        Args:
            directory_path: Path to the directory to analyze
            recursive: Whether to search subdirectories
            file_patterns: List of file patterns to include (e.g., ['*.py', '*.java'])
            
        Returns:
            List of FileMetrics objects for all analyzed files
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        results = []
        
        # Get all supported file extensions
        supported_extensions = set()
        for parser in self.parsers:
            supported_extensions.update(parser.supported_extensions)
        
        # Build search patterns
        if file_patterns:
            patterns = file_patterns
        else:
            patterns = [f"*{ext}" for ext in supported_extensions]
        
        # Find files
        files_to_analyze = []
        for pattern in patterns:
            if recursive:
                search_pattern = os.path.join(directory_path, "**", pattern)
                files_to_analyze.extend(glob.glob(search_pattern, recursive=True))
            else:
                search_pattern = os.path.join(directory_path, pattern)
                files_to_analyze.extend(glob.glob(search_pattern))
        
        # Remove duplicates and sort
        files_to_analyze = sorted(set(files_to_analyze))
        
        # Analyze each file
        for filepath in files_to_analyze:
            if os.path.isfile(filepath):
                metrics = self.analyze_file(filepath)
                if metrics:
                    results.append(metrics)
        
        return results
    
    def generate_summary_report(self, file_metrics_list: List[FileMetrics]) -> Dict[str, Any]:
        """
        Generate a summary report from multiple file analyses.
        
        Args:
            file_metrics_list: List of FileMetrics objects
            
        Returns:
            Dictionary containing summary statistics and aggregated metrics
        """
        if not file_metrics_list:
            return {
                'total_files': 0,
                'total_functions': 0,
                'total_classes': 0,
                'total_loc': 0,
                'average_complexity': 0,
                'average_maintainability': 0,
                'complexity_distribution': {},
                'quality_assessment': 'No files analyzed'
            }
        
        # Aggregate statistics
        total_files = len(file_metrics_list)
        total_functions = sum(len(fm.functions) for fm in file_metrics_list)
        total_classes = sum(len(fm.classes) for fm in file_metrics_list)
        total_loc = sum(fm.lines_of_code for fm in file_metrics_list)
        
        # Calculate averages
        all_functions = []
        for fm in file_metrics_list:
            all_functions.extend(fm.functions)
        
        if all_functions:
            average_complexity = sum(f.cyclomatic_complexity for f in all_functions) / len(all_functions)
            complexity_values = [f.cyclomatic_complexity for f in all_functions]
            
            # Complexity distribution
            complexity_distribution = {
                'simple (1-5)': len([c for c in complexity_values if 1 <= c <= 5]),
                'moderate (6-10)': len([c for c in complexity_values if 6 <= c <= 10]),
                'complex (11-20)': len([c for c in complexity_values if 11 <= c <= 20]),
                'very_complex (21+)': len([c for c in complexity_values if c > 20])
            }
        else:
            average_complexity = 0
            complexity_distribution = {}
        
        maintainability_values = [fm.maintainability_index for fm in file_metrics_list]
        average_maintainability = sum(maintainability_values) / len(maintainability_values)
        
        # Quality assessment
        quality_assessment = self._assess_overall_quality(
            average_complexity, average_maintainability, file_metrics_list
        )
        
        # Find problematic files
        problematic_files = self._identify_problematic_files(file_metrics_list)
        
        return {
            'total_files': total_files,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'total_loc': total_loc,
            'average_complexity': round(average_complexity, 2),
            'average_maintainability': round(average_maintainability, 2),
            'complexity_distribution': complexity_distribution,
            'quality_assessment': quality_assessment,
            'problematic_files': problematic_files,
            'file_breakdown': self._generate_file_breakdown(file_metrics_list)
        }
    
    def _get_parser_for_file(self, filepath: str) -> Optional[BaseParser]:
        """Find the appropriate parser for a given file"""
        for parser in self.parsers:
            if parser.can_parse(filepath):
                return parser
        return None
    
    def _assess_overall_quality(self, avg_complexity: float, avg_maintainability: float, 
                              file_metrics: List[FileMetrics]) -> str:
        """Assess overall code quality based on metrics"""
        quality_score = 0
        
        # Complexity assessment (40% weight)
        if avg_complexity <= 5:
            quality_score += 40
        elif avg_complexity <= 10:
            quality_score += 30
        elif avg_complexity <= 15:
            quality_score += 20
        else:
            quality_score += 10
        
        # Maintainability assessment (40% weight)
        if avg_maintainability >= 85:
            quality_score += 40
        elif avg_maintainability >= 70:
            quality_score += 30
        elif avg_maintainability >= 50:
            quality_score += 20
        else:
            quality_score += 10
        
        # Function size assessment (20% weight)
        all_functions = []
        for fm in file_metrics:
            all_functions.extend(fm.functions)
        
        if all_functions:
            avg_function_size = sum(f.lines_of_code for f in all_functions) / len(all_functions)
            if avg_function_size <= 50:
                quality_score += 20
            elif avg_function_size <= 100:
                quality_score += 15
            else:
                quality_score += 5
        else:
            quality_score += 20  # No functions to penalize
        
        # Return quality assessment
        if quality_score >= 90:
            return "Excellent"
        elif quality_score >= 70:
            return "Good"
        elif quality_score >= 50:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _identify_problematic_files(self, file_metrics: List[FileMetrics]) -> List[Dict[str, Any]]:
        """Identify files that need attention"""
        problematic = []
        
        for fm in file_metrics:
            issues = []
            
            # Check maintainability
            if fm.maintainability_index < 50:
                issues.append("Low maintainability")
            
            # Check for complex functions
            complex_functions = [f for f in fm.functions if f.cyclomatic_complexity > 15]
            if complex_functions:
                issues.append(f"High complexity functions: {len(complex_functions)}")
            
            # Check for large functions
            large_functions = [f for f in fm.functions if f.lines_of_code > 100]
            if large_functions:
                issues.append(f"Large functions: {len(large_functions)}")
            
            if issues:
                problematic.append({
                    'filepath': fm.filepath,
                    'maintainability_index': round(fm.maintainability_index, 2),
                    'issues': issues
                })
        
        # Sort by maintainability index (worst first)
        problematic.sort(key=lambda x: x['maintainability_index'])
        
        return problematic[:10]  # Return top 10 most problematic files
    
    def _generate_file_breakdown(self, file_metrics: List[FileMetrics]) -> List[Dict[str, Any]]:
        """Generate per-file breakdown of metrics"""
        breakdown = []
        
        for fm in file_metrics:
            avg_complexity = (sum(f.cyclomatic_complexity for f in fm.functions) / 
                            len(fm.functions)) if fm.functions else 0
            
            breakdown.append({
                'filepath': fm.filepath,
                'loc': fm.lines_of_code,
                'functions': len(fm.functions),
                'classes': len(fm.classes),
                'avg_complexity': round(avg_complexity, 2),
                'maintainability': round(fm.maintainability_index, 2)
            })
        
        return breakdown
