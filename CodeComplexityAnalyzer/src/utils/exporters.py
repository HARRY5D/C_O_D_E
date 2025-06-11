"""
Export functionality for different output formats.
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

from core.parsers.base_parser import FileMetrics, FunctionMetrics


class BaseExporter:
    """Base class for all exporters"""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
    
    def export(self, file_metrics: List[FileMetrics], summary: Dict[str, Any], 
               output_path: str) -> None:
        """Export metrics to specified format"""
        raise NotImplementedError


class JsonExporter(BaseExporter):
    """Export analysis results to JSON format"""
    
    def export(self, file_metrics: List[FileMetrics], summary: Dict[str, Any], 
               output_path: str) -> None:
        """Export to JSON file"""
        data = self._prepare_data(file_metrics, summary)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _prepare_data(self, file_metrics: List[FileMetrics], summary: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare data for JSON export"""
        
        files_data = []
        for fm in file_metrics:
            functions_data = []
            for func in fm.functions:
                functions_data.append({
                    'name': func.name,
                    'start_line': func.start_line,
                    'end_line': func.end_line,
                    'lines_of_code': func.lines_of_code,
                    'cyclomatic_complexity': func.cyclomatic_complexity,
                    'nesting_depth': func.nesting_depth,
                    'parameters': func.parameters,
                    'halstead_difficulty': func.halstead_difficulty,
                    'halstead_effort': func.halstead_effort,
                    'halstead_volume': func.halstead_volume
                })
            
            files_data.append({
                'filepath': fm.filepath,
                'total_lines': fm.total_lines,
                'lines_of_code': fm.lines_of_code,
                'blank_lines': fm.blank_lines,
                'comment_lines': fm.comment_lines,
                'maintainability_index': fm.maintainability_index,
                'functions': functions_data,
                'classes': fm.classes
            })
        
        return {
            'metadata': {
                'export_timestamp': self.timestamp,
                'analyzer_version': '1.0.0',
                'total_files_analyzed': len(file_metrics)
            },
            'summary': summary,
            'files': files_data
        }
    
    def _format_json(self, data: Dict[str, Any]) -> str:
        """Format data as JSON string"""
        return json.dumps(data, indent=2, ensure_ascii=False)


class CsvExporter(BaseExporter):
    """Export analysis results to CSV format"""
    
    def export(self, file_metrics: List[FileMetrics], summary: Dict[str, Any], 
               output_path: str) -> None:
        """Export to CSV file"""
        csv_data = self._prepare_csv_data(file_metrics)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            f.write(csv_data)
    
    def _prepare_csv_data(self, file_metrics: List[FileMetrics]) -> str:
        """Prepare data for CSV export"""
        
        # Prepare function-level data
        function_rows = []
        
        for fm in file_metrics:
            for func in fm.functions:
                function_rows.append({
                    'File': fm.filepath,
                    'Function': func.name,
                    'Start Line': func.start_line,
                    'End Line': func.end_line,
                    'Lines of Code': func.lines_of_code,
                    'Cyclomatic Complexity': func.cyclomatic_complexity,
                    'Nesting Depth': func.nesting_depth,
                    'Parameters': func.parameters,
                    'File Maintainability': round(fm.maintainability_index, 2)
                })
        
        if not function_rows:
            # If no functions, create file-level summary
            file_rows = []
            for fm in file_metrics:
                file_rows.append({
                    'File': fm.filepath,
                    'Total Lines': fm.total_lines,
                    'Lines of Code': fm.lines_of_code,
                    'Blank Lines': fm.blank_lines,
                    'Comment Lines': fm.comment_lines,
                    'Functions': len(fm.functions),
                    'Classes': len(fm.classes),
                    'Maintainability Index': round(fm.maintainability_index, 2)
                })
            
            df = pd.DataFrame(file_rows)
        else:
            df = pd.DataFrame(function_rows)
        
        return df.to_csv(index=False)


class HtmlExporter(BaseExporter):
    """Export analysis results to HTML format"""
    
    def export(self, file_metrics: List[FileMetrics], summary: Dict[str, Any], 
               output_path: str) -> None:
        """Export to HTML file"""
        html_content = self._generate_html(file_metrics, summary)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _generate_html(self, file_metrics: List[FileMetrics], summary: Dict[str, Any]) -> str:
        """Generate HTML report"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Complexity Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1, h2, h3 {{
            color: #333;
        }}
        h1 {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #007bff;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        .high-complexity {{
            background-color: #ffebee !important;
        }}
        .medium-complexity {{
            background-color: #fff3e0 !important;
        }}
        .good {{
            color: #28a745;
        }}
        .warning {{
            color: #ffc107;
        }}
        .danger {{
            color: #dc3545;
        }}
        .file-section {{
            margin: 30px 0;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
        }}
        .file-header {{
            background-color: #007bff;
            color: white;
            padding: 15px;
            font-weight: bold;
        }}
        .file-content {{
            padding: 20px;
        }}
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Code Complexity Analysis Report</h1>
        
        <div class="summary">
            <div class="metric-card">
                <div class="metric-value">{summary['total_files']}</div>
                <div class="metric-label">Total Files</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['total_functions']}</div>
                <div class="metric-label">Total Functions</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['total_loc']:,}</div>
                <div class="metric-label">Lines of Code</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['average_complexity']:.1f}</div>
                <div class="metric-label">Avg Complexity</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary['average_maintainability']:.1f}</div>
                <div class="metric-label">Avg Maintainability</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {self._get_quality_class(summary['quality_assessment'])}">{summary['quality_assessment']}</div>
                <div class="metric-label">Quality Assessment</div>
            </div>
        </div>
        
        <h2>📈 Complexity Distribution</h2>
        <table>
            <thead>
                <tr>
                    <th>Complexity Range</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
            </thead>
            <tbody>
        """
        
        # Add complexity distribution
        total_functions = sum(summary['complexity_distribution'].values()) if summary['complexity_distribution'] else 0
        for category, count in summary.get('complexity_distribution', {}).items():
            percentage = (count / total_functions * 100) if total_functions > 0 else 0
            html += f"""
                <tr>
                    <td>{category.replace('_', ' ').title()}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
            """
        
        html += """
            </tbody>
        </table>
        
        <h2>📂 File Analysis</h2>
        """
        
        # Add file details
        for fm in file_metrics:
            avg_complexity = (sum(f.cyclomatic_complexity for f in fm.functions) / 
                            len(fm.functions)) if fm.functions else 0
            
            html += f"""
            <div class="file-section">
                <div class="file-header">
                    📁 {os.path.basename(fm.filepath)}
                </div>
                <div class="file-content">
                    <p><strong>Path:</strong> {fm.filepath}</p>
                    <p><strong>Lines of Code:</strong> {fm.lines_of_code}</p>
                    <p><strong>Functions:</strong> {len(fm.functions)}</p>
                    <p><strong>Classes:</strong> {len(fm.classes)}</p>
                    <p><strong>Maintainability Index:</strong> 
                        <span class="{self._get_maintainability_class(fm.maintainability_index)}">
                            {fm.maintainability_index:.1f}
                        </span>
                    </p>
                    
                    <h4>Functions</h4>
                    <table>
                        <thead>
                            <tr>
                                <th>Function</th>
                                <th>LOC</th>
                                <th>Complexity</th>
                                <th>Nesting</th>
                                <th>Parameters</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for func in fm.functions:
                complexity_class = self._get_complexity_class(func.cyclomatic_complexity)
                html += f"""
                            <tr class="{complexity_class}">
                                <td>{func.name}</td>
                                <td>{func.lines_of_code}</td>
                                <td>{func.cyclomatic_complexity}</td>
                                <td>{func.nesting_depth}</td>
                                <td>{func.parameters}</td>
                            </tr>
                """
            
            if not fm.functions:
                html += """
                            <tr>
                                <td colspan="5">No functions found</td>
                            </tr>
                """
            
            html += """
                        </tbody>
                    </table>
                </div>
            </div>
            """
        
        html += f"""
        <div class="timestamp">
            Report generated on {self.timestamp}
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def _get_quality_class(self, quality: str) -> str:
        """Get CSS class for quality assessment"""
        quality_classes = {
            "Excellent": "good",
            "Good": "good",
            "Fair": "warning",
            "Needs Improvement": "danger"
        }
        return quality_classes.get(quality, "")
    
    def _get_maintainability_class(self, mi: float) -> str:
        """Get CSS class for maintainability index"""
        if mi >= 80:
            return "good"
        elif mi >= 60:
            return "warning"
        else:
            return "danger"
    
    def _get_complexity_class(self, complexity: int) -> str:
        """Get CSS class for complexity level"""
        if complexity >= 15:
            return "high-complexity"
        elif complexity >= 10:
            return "medium-complexity"
        else:
            return ""


class TextExporter(BaseExporter):
    """Export analysis results to plain text format"""
    
    def export(self, file_metrics: List[FileMetrics], summary: Dict[str, Any], 
               output_path: str) -> None:
        """Export to text file"""
        content = self._generate_text_report(file_metrics, summary)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_text_report(self, file_metrics: List[FileMetrics], summary: Dict[str, Any]) -> str:
        """Generate plain text report"""
        
        lines = [
            "=" * 70,
            "CODE COMPLEXITY ANALYSIS REPORT",
            "=" * 70,
            f"Generated: {self.timestamp}",
            "",
            "SUMMARY",
            "-" * 30,
            f"Total Files: {summary['total_files']}",
            f"Total Functions: {summary['total_functions']}",
            f"Total Classes: {summary['total_classes']}",
            f"Total Lines of Code: {summary['total_loc']:,}",
            f"Average Complexity: {summary['average_complexity']:.2f}",
            f"Average Maintainability: {summary['average_maintainability']:.2f}",
            f"Quality Assessment: {summary['quality_assessment']}",
            "",
        ]
        
        # Complexity distribution
        if summary['complexity_distribution']:
            lines.extend([
                "COMPLEXITY DISTRIBUTION",
                "-" * 30,
            ])
            
            for category, count in summary['complexity_distribution'].items():
                lines.append(f"{category.replace('_', ' ').title()}: {count}")
            
            lines.append("")
        
        # File details
        lines.extend([
            "FILE ANALYSIS",
            "-" * 30,
        ])
        
        for fm in file_metrics:
            lines.extend([
                f"\nFile: {fm.filepath}",
                f"  Lines of Code: {fm.lines_of_code}",
                f"  Functions: {len(fm.functions)}",
                f"  Classes: {len(fm.classes)}",
                f"  Maintainability Index: {fm.maintainability_index:.1f}",
            ])
            
            if fm.functions:
                lines.append("  Functions:")
                for func in fm.functions:
                    complexity_indicator = "⚠️" if func.cyclomatic_complexity >= 15 else "✓" if func.cyclomatic_complexity <= 5 else "!"
                    lines.append(f"    {complexity_indicator} {func.name}: CC={func.cyclomatic_complexity}, LOC={func.lines_of_code}")
        
        # Problematic files
        if summary.get('problematic_files'):
            lines.extend([
                "",
                "FILES NEEDING ATTENTION",
                "-" * 30,
            ])
            
            for pf in summary['problematic_files'][:10]:
                lines.append(f"  • {os.path.basename(pf['filepath'])} (MI: {pf['maintainability_index']:.1f})")
                for issue in pf['issues']:
                    lines.append(f"    - {issue}")
        
        return "\n".join(lines)
