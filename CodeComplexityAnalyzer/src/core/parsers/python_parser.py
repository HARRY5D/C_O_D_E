"""
Python language parser using AST (Abstract Syntax Tree).
"""

import ast
import os
from typing import Dict, List, Set
from collections import defaultdict
import math

from .base_parser import BaseParser, FunctionMetrics, FileMetrics


class PythonParser(BaseParser):
    """Parser for Python source files using AST analysis"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.py', '.pyw']
    
    def can_parse(self, filepath: str) -> bool:
        """Check if this parser can handle Python files"""
        _, ext = os.path.splitext(filepath)
        return ext.lower() in self.supported_extensions
    
    def parse_file(self, filepath: str) -> FileMetrics:
        """Parse a Python file and extract metrics"""
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            raise ValueError(f"Cannot read file {filepath}: {e}")
        
        # Parse AST
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            raise ValueError(f"Syntax error in {filepath}: {e}")
        
        # Count lines
        total_lines, lines_of_code, blank_lines, comment_lines = self._count_lines(content)
        
        # Extract functions and classes
        visitor = PythonASTVisitor(content)
        visitor.visit(tree)
        
        # Calculate maintainability index
        maintainability_index = self._calculate_maintainability_index(
            lines_of_code, visitor.functions, visitor.cyclomatic_complexity
        )
        
        return FileMetrics(
            filepath=filepath,
            total_lines=total_lines,
            lines_of_code=lines_of_code,
            blank_lines=blank_lines,
            comment_lines=comment_lines,
            functions=visitor.functions,
            classes=visitor.classes,
            maintainability_index=maintainability_index
        )
    
    def _is_comment_line(self, line: str) -> bool:
        """Check if a line is a Python comment"""
        return line.startswith('#')
    
    def _calculate_maintainability_index(self, loc: int, functions: List[FunctionMetrics], 
                                       total_complexity: int) -> float:
        """
        Calculate Maintainability Index using the formula:
        MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
        
        Where:
        - HV = Halstead Volume (approximated)
        - CC = Cyclomatic Complexity
        - LOC = Lines of Code
        """
        if loc == 0:
            return 100.0
        
        # Approximate Halstead Volume (since we don't have exact operators/operands count)
        halstead_volume = max(1, loc * 8.0)  # Rough approximation
        
        # Use average complexity if we have functions
        avg_complexity = total_complexity / max(1, len(functions)) if functions else 1
        
        try:
            mi = 171 - 5.2 * math.log(halstead_volume) - 0.23 * avg_complexity - 16.2 * math.log(loc)
            return max(0, min(100, mi))  # Clamp between 0 and 100
        except ValueError:
            return 50.0  # Default value if calculation fails


class PythonASTVisitor(ast.NodeVisitor):
    """AST visitor to extract metrics from Python code"""
    
    def __init__(self, content: str):
        self.content = content
        self.lines = content.split('\n')
        self.functions = []
        self.classes = []
        self.cyclomatic_complexity = 0
        self.current_function = None
        self.nesting_depth = 0
        self.max_nesting = 0
        
        # For Halstead metrics
        self.operators = set()
        self.operands = set()
        self.operator_count = defaultdict(int)
        self.operand_count = defaultdict(int)
    
    def visit_FunctionDef(self, node):
        """Visit function definitions"""
        self._visit_function(node)
    
    def visit_AsyncFunctionDef(self, node):
        """Visit async function definitions"""
        self._visit_function(node)
    
    def _visit_function(self, node):
        """Process function/method definitions"""
        # Calculate function metrics
        start_line = node.lineno
        end_line = self._get_end_line(node)
        func_loc = self._count_function_loc(start_line, end_line)
        
        # Calculate cyclomatic complexity for this function
        func_complexity = self._calculate_function_complexity(node)
        
        # Calculate nesting depth
        max_depth = self._calculate_max_nesting_depth(node)
        
        # Count parameters
        param_count = len(node.args.args)
        if node.args.vararg:
            param_count += 1
        if node.args.kwarg:
            param_count += 1
        
        # Create function metrics
        function_metrics = FunctionMetrics(
            name=node.name,
            start_line=start_line,
            end_line=end_line,
            lines_of_code=func_loc,
            cyclomatic_complexity=func_complexity,
            nesting_depth=max_depth,
            parameters=param_count
        )
        
        self.functions.append(function_metrics)
        self.cyclomatic_complexity += func_complexity
        
        # Continue visiting child nodes
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Visit class definitions"""
        self.classes.append(node.name)
        self.generic_visit(node)
    
    def visit_If(self, node):
        """Visit if statements (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_While(self, node):
        """Visit while loops (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_For(self, node):
        """Visit for loops (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        """Visit except handlers (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_With(self, node):
        """Visit with statements (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_AsyncWith(self, node):
        """Visit async with statements (increases complexity)"""
        self.cyclomatic_complexity += 1
        self.generic_visit(node)
    
    def visit_BoolOp(self, node):
        """Visit boolean operations (and/or - increases complexity)"""
        if isinstance(node.op, (ast.And, ast.Or)):
            # Each additional condition adds to complexity
            self.cyclomatic_complexity += len(node.values) - 1
        self.generic_visit(node)
    
    def _get_end_line(self, node):
        """Get the end line of a node"""
        if hasattr(node, 'end_lineno') and node.end_lineno is not None:
            return node.end_lineno
        
        # Fallback: find the last line by traversing all child nodes
        end_line = node.lineno
        for child in ast.walk(node):
            if hasattr(child, 'lineno') and child.lineno is not None:
                end_line = max(end_line, child.lineno)
        return end_line
    
    def _count_function_loc(self, start_line: int, end_line: int) -> int:
        """Count lines of code in a function (excluding blank lines and comments)"""
        loc = 0
        for i in range(start_line - 1, min(end_line, len(self.lines))):
            line = self.lines[i].strip()
            if line and not line.startswith('#'):
                loc += 1
        return loc
    
    def _calculate_function_complexity(self, node) -> int:
        """Calculate cyclomatic complexity for a specific function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, 
                                ast.With, ast.AsyncWith)):
                complexity += 1
            elif isinstance(child, ast.BoolOp) and isinstance(child.op, (ast.And, ast.Or)):
                complexity += len(child.values) - 1
        
        return complexity
    
    def _calculate_max_nesting_depth(self, node) -> int:
        """Calculate maximum nesting depth in a function"""
        def calculate_depth(node, current_depth=0):
            max_depth = current_depth
            
            for child in ast.iter_child_nodes(node):
                child_depth = current_depth
                
                # These constructs increase nesting depth
                if isinstance(child, (ast.If, ast.While, ast.For, ast.With, 
                                    ast.AsyncWith, ast.Try, ast.FunctionDef, 
                                    ast.AsyncFunctionDef, ast.ClassDef)):
                    child_depth += 1
                
                # Recursively check children
                depth = calculate_depth(child, child_depth)
                max_depth = max(max_depth, depth)
            
            return max_depth
        
        return calculate_depth(node)
