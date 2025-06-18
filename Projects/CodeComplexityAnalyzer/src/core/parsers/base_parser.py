"""
Base parser interface for different programming languages.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class FunctionMetrics:
    """Metrics for a single function/method"""
    name: str
    start_line: int
    end_line: int
    lines_of_code: int
    cyclomatic_complexity: int
    nesting_depth: int
    parameters: int
    halstead_difficulty: float = 0.0
    halstead_effort: float = 0.0
    halstead_volume: float = 0.0


@dataclass
class FileMetrics:
    """Metrics for a single file"""
    filepath: str
    total_lines: int
    lines_of_code: int
    blank_lines: int
    comment_lines: int
    functions: List[FunctionMetrics]
    classes: List[str]
    maintainability_index: float = 0.0


class BaseParser(ABC):
    """Abstract base class for language-specific parsers"""
    
    def __init__(self):
        self.supported_extensions = []
    
    @abstractmethod
    def parse_file(self, filepath: str) -> FileMetrics:
        """
        Parse a single file and return its metrics.
        
        Args:
            filepath: Path to the file to analyze
            
        Returns:
            FileMetrics object containing all calculated metrics
        """
        pass
    
    @abstractmethod
    def can_parse(self, filepath: str) -> bool:
        """
        Check if this parser can handle the given file.
        
        Args:
            filepath: Path to the file to check
            
        Returns:
            True if this parser can handle the file, False otherwise
        """
        pass
    
    def _count_lines(self, content: str) -> tuple:
        """
        Count different types of lines in the content.
        
        Args:
            content: File content as string
            
        Returns:
            Tuple of (total_lines, lines_of_code, blank_lines, comment_lines)
        """
        lines = content.split('\n')
        total_lines = len(lines)
        blank_lines = 0
        comment_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif self._is_comment_line(stripped):
                comment_lines += 1
        
        lines_of_code = total_lines - blank_lines - comment_lines
        return total_lines, lines_of_code, blank_lines, comment_lines
    
    @abstractmethod
    def _is_comment_line(self, line: str) -> bool:
        """
        Check if a line is a comment line (language-specific).
        
        Args:
            line: Stripped line content
            
        Returns:
            True if the line is a comment, False otherwise
        """
        pass
