"""
Command Line Interface for the Code Complexity Analyzer.
"""

import click
import os
import sys
from typing import List, Optional
from tabulate import tabulate
from colorama import init, Fore, Style

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from core.analyzer import CodeComplexityAnalyzer
    from utils import exporters
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure you're running from the correct directory.")
    sys.exit(1)

# Initialize colorama for colored output
init(autoreset=True)


@click.group()
def cli():
    """Code Complexity Analyzer - Analyze source code complexity metrics."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, 
              help='Recursively analyze subdirectories')
@click.option('--output', '-o', type=click.Path(), 
              help='Output file path')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'html', 'console']), 
              default='console', help='Output format')
@click.option('--show-functions', is_flag=True, 
              help='Show detailed function metrics')
@click.option('--complexity-threshold', type=int, default=10,
              help='Highlight functions above this complexity threshold')
def analyze(path: str, recursive: bool, output: Optional[str], format: str, 
           show_functions: bool, complexity_threshold: int):
    """Analyze code complexity for a file or directory."""
    
    analyzer = CodeComplexityAnalyzer()
    
    click.echo(f"{Fore.CYAN}Analyzing: {path}{Style.RESET_ALL}")
    
    try:
        # Determine if path is a file or directory
        if os.path.isfile(path):
            file_metrics = analyzer.analyze_file(path)
            if file_metrics:
                results = [file_metrics]
            else:
                click.echo(f"{Fore.RED}Error: Could not analyze file {path}{Style.RESET_ALL}")
                return
        else:
            results = analyzer.analyze_directory(path, recursive=recursive)
            if not results:
                click.echo(f"{Fore.YELLOW}No supported files found in {path}{Style.RESET_ALL}")
                return
        
        # Generate summary report
        summary = analyzer.generate_summary_report(results)
          # Output results based on format
        if format == 'console':
            _display_console_output(results, summary, show_functions, complexity_threshold)
        elif format == 'json':
            exporter = exporters.JsonExporter()
            output_path = output or 'complexity_analysis.json'
            exporter.export(results, summary, output_path)
            click.echo(f"{Fore.GREEN}Results exported to {output_path}{Style.RESET_ALL}")
        elif format == 'csv':
            exporter = exporters.CsvExporter()
            output_path = output or 'complexity_analysis.csv'
            exporter.export(results, summary, output_path)
            click.echo(f"{Fore.GREEN}Results exported to {output_path}{Style.RESET_ALL}")
        elif format == 'html':
            exporter = exporters.HtmlExporter()
            output_path = output or 'complexity_analysis.html'
            exporter.export(results, summary, output_path)
            click.echo(f"{Fore.GREEN}Results exported to {output_path}{Style.RESET_ALL}")
            
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--recursive', '-r', is_flag=True, 
              help='Recursively analyze subdirectories')
@click.option('--threshold', type=int, default=15,
              help='Complexity threshold for highlighting issues')
def report(path: str, recursive: bool, threshold: int):
    """Generate a detailed quality report."""
    
    analyzer = CodeComplexityAnalyzer()
    
    click.echo(f"{Fore.CYAN}Generating quality report for: {path}{Style.RESET_ALL}")
    
    try:
        # Analyze the code
        if os.path.isfile(path):
            file_metrics = analyzer.analyze_file(path)
            results = [file_metrics] if file_metrics else []
        else:
            results = analyzer.analyze_directory(path, recursive=recursive)
        
        if not results:
            click.echo(f"{Fore.YELLOW}No files to analyze{Style.RESET_ALL}")
            return
        
        summary = analyzer.generate_summary_report(results)
        
        # Display detailed report
        _display_quality_report(results, summary, threshold)
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


@cli.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
def compare(file1: str, file2: str):
    """Compare complexity metrics between two files."""
    
    analyzer = CodeComplexityAnalyzer()
    
    try:
        metrics1 = analyzer.analyze_file(file1)
        metrics2 = analyzer.analyze_file(file2)
        
        if not metrics1:
            click.echo(f"{Fore.RED}Error: Could not analyze {file1}{Style.RESET_ALL}")
            return
        if not metrics2:
            click.echo(f"{Fore.RED}Error: Could not analyze {file2}{Style.RESET_ALL}")
            return
        
        _display_comparison(metrics1, metrics2)
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


def _display_console_output(results: List, summary: dict, show_functions: bool, 
                          complexity_threshold: int):
    """Display analysis results in console format."""
    
    # Summary section
    click.echo(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}SUMMARY REPORT{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    summary_data = [
        ["Total Files", summary['total_files']],
        ["Total Functions", summary['total_functions']],
        ["Total Classes", summary['total_classes']],
        ["Total LOC", summary['total_loc']],
        ["Average Complexity", summary['average_complexity']],
        ["Average Maintainability", f"{summary['average_maintainability']:.1f}"],
        ["Quality Assessment", summary['quality_assessment']]
    ]
    
    click.echo(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="grid"))
    
    # Complexity distribution
    if summary['complexity_distribution']:
        click.echo(f"\n{Fore.YELLOW}Complexity Distribution:{Style.RESET_ALL}")
        dist_data = [[k.replace('_', ' ').title(), v] for k, v in summary['complexity_distribution'].items()]
        click.echo(tabulate(dist_data, headers=["Complexity Range", "Count"], tablefmt="grid"))
    
    # File-by-file breakdown
    click.echo(f"\n{Fore.CYAN}FILE BREAKDOWN{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
    
    for fm in results:
        color = Fore.GREEN
        if fm.maintainability_index < 50:
            color = Fore.RED
        elif fm.maintainability_index < 70:
            color = Fore.YELLOW
        
        click.echo(f"\n{color}File: {fm.filepath}{Style.RESET_ALL}")
        
        file_data = [
            ["Lines of Code", fm.lines_of_code],
            ["Functions", len(fm.functions)],
            ["Classes", len(fm.classes)],
            ["Maintainability Index", f"{fm.maintainability_index:.1f}"]
        ]
        
        click.echo(tabulate(file_data, headers=["Metric", "Value"], tablefmt="simple"))
        
        if show_functions and fm.functions:
            click.echo(f"\n{Fore.YELLOW}  Functions:{Style.RESET_ALL}")
            
            func_data = []
            for func in fm.functions:
                color_prefix = ""
                if func.cyclomatic_complexity >= complexity_threshold:
                    color_prefix = f"{Fore.RED}⚠ {Style.RESET_ALL}"
                
                func_data.append([
                    f"{color_prefix}{func.name}",
                    func.lines_of_code,
                    func.cyclomatic_complexity,
                    func.nesting_depth,
                    func.parameters
                ])
            
            click.echo(tabulate(func_data, 
                              headers=["Function", "LOC", "Complexity", "Nesting", "Params"],
                              tablefmt="simple"))
    
    # Problematic files
    if summary['problematic_files']:
        click.echo(f"\n{Fore.RED}FILES NEEDING ATTENTION{Style.RESET_ALL}")
        click.echo(f"{Fore.RED}{'-'*60}{Style.RESET_ALL}")
        
        for prob_file in summary['problematic_files'][:5]:  # Show top 5
            click.echo(f"\n{Fore.RED}⚠ {prob_file['filepath']}{Style.RESET_ALL}")
            click.echo(f"  Maintainability: {prob_file['maintainability_index']}")
            for issue in prob_file['issues']:
                click.echo(f"  • {issue}")


def _display_quality_report(results: List, summary: dict, threshold: int):
    """Display a detailed quality assessment report."""
    
    click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}CODE QUALITY ASSESSMENT REPORT{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    # Overall assessment
    quality = summary['quality_assessment']
    if quality == "Excellent":
        color = Fore.GREEN
    elif quality in ["Good", "Fair"]:
        color = Fore.YELLOW
    else:
        color = Fore.RED
    
    click.echo(f"\n{color}Overall Quality: {quality}{Style.RESET_ALL}")
    click.echo(f"Average Complexity: {summary['average_complexity']}")
    click.echo(f"Average Maintainability: {summary['average_maintainability']:.1f}")
    
    # Detailed recommendations
    click.echo(f"\n{Fore.YELLOW}RECOMMENDATIONS{Style.RESET_ALL}")
    click.echo(f"{Fore.YELLOW}{'-'*50}{Style.RESET_ALL}")
    
    # Find high-complexity functions across all files
    high_complexity_functions = []
    for fm in results:
        for func in fm.functions:
            if func.cyclomatic_complexity >= threshold:
                high_complexity_functions.append((fm.filepath, func))
    
    if high_complexity_functions:
        click.echo(f"\n{Fore.RED}High Complexity Functions (>= {threshold}){Style.RESET_ALL}")
        for filepath, func in high_complexity_functions[:10]:  # Top 10
            rel_path = os.path.relpath(filepath)
            click.echo(f"  • {rel_path}::{func.name} (CC: {func.cyclomatic_complexity})")
    
    # Files with low maintainability
    low_maintainability = [fm for fm in results if fm.maintainability_index < 60]
    if low_maintainability:
        click.echo(f"\n{Fore.RED}Low Maintainability Files{Style.RESET_ALL}")
        for fm in low_maintainability[:5]:
            rel_path = os.path.relpath(fm.filepath)
            click.echo(f"  • {rel_path} (MI: {fm.maintainability_index:.1f})")
    
    # General recommendations
    click.echo(f"\n{Fore.CYAN}General Recommendations:{Style.RESET_ALL}")
    if summary['average_complexity'] > 10:
        click.echo("  • Consider breaking down complex functions")
    if summary['average_maintainability'] < 70:
        click.echo("  • Focus on improving code maintainability")
    if any(len(fm.functions) == 0 for fm in results):
        click.echo("  • Some files have no functions - consider code organization")
    
    click.echo("  • Add unit tests for complex functions")
    click.echo("  • Consider using static analysis tools in CI/CD")
    click.echo("  • Implement code review practices")


def _display_comparison(metrics1, metrics2):
    """Display comparison between two files."""
    
    click.echo(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}FILE COMPARISON{Style.RESET_ALL}")
    click.echo(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    
    file1_name = os.path.basename(metrics1.filepath)
    file2_name = os.path.basename(metrics2.filepath)
    
    # Basic metrics comparison
    comparison_data = [
        ["Metric", file1_name, file2_name, "Difference"],
        ["Lines of Code", metrics1.lines_of_code, metrics2.lines_of_code, 
         metrics2.lines_of_code - metrics1.lines_of_code],
        ["Functions", len(metrics1.functions), len(metrics2.functions),
         len(metrics2.functions) - len(metrics1.functions)],
        ["Classes", len(metrics1.classes), len(metrics2.classes),
         len(metrics2.classes) - len(metrics1.classes)],
        ["Maintainability", f"{metrics1.maintainability_index:.1f}", 
         f"{metrics2.maintainability_index:.1f}",
         f"{metrics2.maintainability_index - metrics1.maintainability_index:.1f}"]
    ]
    
    # Calculate average complexity
    avg_complexity1 = (sum(f.cyclomatic_complexity for f in metrics1.functions) / 
                      len(metrics1.functions)) if metrics1.functions else 0
    avg_complexity2 = (sum(f.cyclomatic_complexity for f in metrics2.functions) / 
                      len(metrics2.functions)) if metrics2.functions else 0
    
    comparison_data.append([
        "Avg Complexity", f"{avg_complexity1:.1f}", f"{avg_complexity2:.1f}",
        f"{avg_complexity2 - avg_complexity1:.1f}"
    ])
    
    click.echo(tabulate(comparison_data[1:], headers=comparison_data[0], tablefmt="grid"))
    
    # Winner determination
    click.echo(f"\n{Fore.YELLOW}Analysis:{Style.RESET_ALL}")
    if metrics2.maintainability_index > metrics1.maintainability_index:
        click.echo(f"  {file2_name} has better maintainability")
    elif metrics1.maintainability_index > metrics2.maintainability_index:
        click.echo(f"  {file1_name} has better maintainability")
    else:
        click.echo(f"  Both files have similar maintainability")
    
    if avg_complexity2 < avg_complexity1:
        click.echo(f"  {file2_name} has lower complexity")
    elif avg_complexity1 < avg_complexity2:
        click.echo(f"  {file1_name} has lower complexity")
    else:
        click.echo(f"  Both files have similar complexity")


if __name__ == '__main__':
    cli()
