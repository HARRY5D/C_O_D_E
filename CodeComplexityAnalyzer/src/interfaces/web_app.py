"""
Streamlit Web Interface for the Code Complexity Analyzer.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import tempfile
import sys
from typing import List

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.analyzer import CodeComplexityAnalyzer
from core.parsers.base_parser import FileMetrics
from utils.exporters import JsonExporter, CsvExporter


def main():
    """Main Streamlit application"""
    
    st.set_page_config(
        page_title="Code Complexity Analyzer",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("📊 Code Complexity Analyzer")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Analysis Options")
    
    # Analysis mode selection
    analysis_mode = st.sidebar.selectbox(
        "Analysis Mode",
        ["Upload Files", "Directory Analysis", "Sample Analysis"]
    )
    
    analyzer = CodeComplexityAnalyzer()
    
    if analysis_mode == "Upload Files":
        handle_file_upload(analyzer)
    elif analysis_mode == "Directory Analysis":
        handle_directory_analysis(analyzer)
    else:
        handle_sample_analysis(analyzer)


def handle_file_upload(analyzer: CodeComplexityAnalyzer):
    """Handle file upload analysis"""
    
    st.header("📁 File Upload Analysis")
    
    uploaded_files = st.file_uploader(
        "Upload Python files for analysis",
        type=['py'],
        accept_multiple_files=True,
        help="Upload one or more Python files to analyze their complexity metrics"
    )
    
    if uploaded_files:
        st.info(f"Uploaded {len(uploaded_files)} file(s)")
        if st.button("Analyze Files", type="primary"):
            with st.spinner("Analyzing files..."):
                results = []
                
                for uploaded_file in uploaded_files:
                    try:
                        # Get file content
                        if uploaded_file is not None:
                            # Read the content as string
                            content = uploaded_file.getvalue()
                            
                            # Handle both string and bytes content
                            if isinstance(content, bytes):
                                try:
                                    content = content.decode('utf-8')
                                except UnicodeDecodeError:
                                    st.error(f"Error: {uploaded_file.name} contains non-UTF-8 characters")
                                    continue
                            
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as tmp_file:
                                tmp_file.write(content)
                                tmp_file_path = tmp_file.name
                            
                            try:
                                metrics = analyzer.analyze_file(tmp_file_path)
                                if metrics:
                                    # Update filepath to show original name
                                    metrics.filepath = uploaded_file.name
                                    results.append(metrics)
                                    st.success(f"✅ Successfully analyzed {uploaded_file.name}")
                                else:
                                    st.warning(f"⚠️ Could not analyze {uploaded_file.name} - may not be valid Python code")
                            except Exception as e:
                                st.error(f"❌ Error analyzing {uploaded_file.name}: {str(e)}")
                            finally:
                                # Clean up temporary file
                                try:
                                    os.unlink(tmp_file_path)
                                except:
                                    pass  # Ignore cleanup errors
                        
                    except Exception as e:
                        st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
                
                if results:
                    display_analysis_results(results, analyzer)
                else:
                    st.error("No files could be analyzed successfully")


def handle_directory_analysis(analyzer: CodeComplexityAnalyzer):
    """Handle directory analysis"""
    
    st.header("📂 Directory Analysis")
    
    # Directory path input
    directory_path = st.text_input(
        "Directory Path",
        placeholder="Enter the path to analyze (e.g., C:/Users/yourname/project)",
        help="Enter the full path to the directory you want to analyze"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        recursive = st.checkbox("Recursive Analysis", value=True,
                              help="Include subdirectories in the analysis")
    
    with col2:
        file_patterns = st.multiselect(
            "File Patterns",
            options=["*.py", "*.java", "*.cpp", "*.js"],
            default=["*.py"],
            help="Select file patterns to include in the analysis"
        )
    
    if directory_path and st.button("Analyze Directory", type="primary"):
        if not os.path.exists(directory_path):
            st.error("Directory does not exist!")
            return
        
        with st.spinner("Analyzing directory..."):
            try:
                results = analyzer.analyze_directory(
                    directory_path, 
                    recursive=recursive,
                    file_patterns=file_patterns if file_patterns else None
                )
                
                if results:
                    display_analysis_results(results, analyzer)
                else:
                    st.warning("No supported files found in the specified directory")
                    
            except Exception as e:
                st.error(f"Error analyzing directory: {e}")


def handle_sample_analysis(analyzer: CodeComplexityAnalyzer):
    """Handle sample code analysis"""
    
    st.header("✍️ Sample Code Analysis")
    st.markdown("Paste your Python code below to analyze its complexity:")
    
    # Code input
    sample_code = st.text_area(
        "Python Code",
        height=300,
        placeholder="""def example_function(x, y):
    if x > 0:
        for i in range(x):
            if i % 2 == 0:
                y += i
            else:
                y -= i
    return y

class ExampleClass:
    def __init__(self):
        self.value = 0
    
    def complex_method(self, data):
        result = []
        for item in data:
            if isinstance(item, str):
                if len(item) > 5:
                    result.append(item.upper())
                else:
                    result.append(item.lower())
            elif isinstance(item, int):
                if item > 0:
                    result.append(item * 2)
                else:
                    result.append(0)
        return result""",
        help="Enter your Python code here"
    )
    
    if sample_code.strip() and st.button("Analyze Code", type="primary"):
        with st.spinner("Analyzing code..."):
            # Save code to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
                tmp_file.write(sample_code)
                tmp_file_path = tmp_file.name
            
            try:
                metrics = analyzer.analyze_file(tmp_file_path)
                if metrics:
                    metrics.filepath = "sample_code.py"
                    display_analysis_results([metrics], analyzer)
                else:
                    st.error("Could not analyze the provided code")
            except Exception as e:
                st.error(f"Error analyzing code: {e}")
            finally:
                os.unlink(tmp_file_path)


def display_analysis_results(results: List[FileMetrics], analyzer: CodeComplexityAnalyzer):
    """Display analysis results with visualizations"""
    
    # Generate summary
    summary = analyzer.generate_summary_report(results)
    
    # Summary metrics
    st.header("📈 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Files", summary['total_files'])
    with col2:
        st.metric("Total Functions", summary['total_functions'])
    with col3:
        st.metric("Total LOC", summary['total_loc'])
    with col4:
        quality_color = get_quality_color(summary['quality_assessment'])
        st.metric("Quality Assessment", summary['quality_assessment'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Complexity", f"{summary['average_complexity']:.1f}")
    with col2:
        st.metric("Avg Maintainability", f"{summary['average_maintainability']:.1f}")
    
    # Visualizations
    st.header("📊 Visualizations")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Functions", "Files", "Export"])
    
    with tab1:
        display_overview_charts(results, summary)
    
    with tab2:
        display_function_analysis(results)
    
    with tab3:
        display_file_analysis(results)
    
    with tab4:
        display_export_options(results, summary)


def display_overview_charts(results: List[FileMetrics], summary: dict):
    """Display overview charts"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Complexity distribution pie chart
        if summary['complexity_distribution']:
            fig = px.pie(
                values=list(summary['complexity_distribution'].values()),
                names=[k.replace('_', ' ').title() for k in summary['complexity_distribution'].keys()],
                title="Complexity Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Maintainability vs Complexity scatter
        if results:
            file_data = []
            for fm in results:
                avg_complexity = (sum(f.cyclomatic_complexity for f in fm.functions) / 
                                len(fm.functions)) if fm.functions else 0
                file_data.append({
                    'File': os.path.basename(fm.filepath),
                    'Maintainability': fm.maintainability_index,
                    'Average Complexity': avg_complexity,
                    'LOC': fm.lines_of_code
                })
            
            df = pd.DataFrame(file_data)
            
            fig = px.scatter(
                df, 
                x='Average Complexity', 
                y='Maintainability',
                size='LOC',
                hover_name='File',
                title="Maintainability vs Complexity",
                labels={'Average Complexity': 'Avg Complexity', 'Maintainability': 'Maintainability Index'}
            )
            
            # Add quadrant lines
            fig.add_hline(y=70, line_dash="dash", line_color="orange", 
                         annotation_text="Good Maintainability Threshold")
            fig.add_vline(x=10, line_dash="dash", line_color="red", 
                         annotation_text="High Complexity Threshold")
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Metrics comparison bar chart
    if len(results) > 1:
        file_comparison_data = []
        for fm in results:
            avg_complexity = (sum(f.cyclomatic_complexity for f in fm.functions) / 
                            len(fm.functions)) if fm.functions else 0
            file_comparison_data.append({
                'File': os.path.basename(fm.filepath),
                'LOC': fm.lines_of_code,
                'Functions': len(fm.functions),
                'Avg Complexity': avg_complexity,
                'Maintainability': fm.maintainability_index
            })
        
        df = pd.DataFrame(file_comparison_data)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Lines of Code', 'Number of Functions', 
                          'Average Complexity', 'Maintainability Index'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # LOC
        fig.add_trace(
            go.Bar(x=df['File'], y=df['LOC'], name='LOC', marker_color='lightblue'),
            row=1, col=1
        )
        
        # Functions
        fig.add_trace(
            go.Bar(x=df['File'], y=df['Functions'], name='Functions', marker_color='lightgreen'),
            row=1, col=2
        )
        
        # Complexity
        fig.add_trace(
            go.Bar(x=df['File'], y=df['Avg Complexity'], name='Avg Complexity', marker_color='orange'),
            row=2, col=1
        )
        
        # Maintainability
        fig.add_trace(
            go.Bar(x=df['File'], y=df['Maintainability'], name='Maintainability', marker_color='lightcoral'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="File Comparison")
        st.plotly_chart(fig, use_container_width=True)


def display_function_analysis(results: List[FileMetrics]):
    """Display function-level analysis"""
    
    st.subheader("🔧 Function Analysis")
    
    # Collect all functions
    all_functions = []
    for fm in results:
        for func in fm.functions:
            all_functions.append({
                'File': os.path.basename(fm.filepath),
                'Function': func.name,
                'LOC': func.lines_of_code,
                'Complexity': func.cyclomatic_complexity,
                'Nesting Depth': func.nesting_depth,
                'Parameters': func.parameters,
                'Full Path': fm.filepath
            })
    
    if not all_functions:
        st.warning("No functions found in the analyzed files")
        return
    
    df = pd.DataFrame(all_functions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Complexity threshold filter
        complexity_threshold = st.slider(
            "Complexity Threshold", 
            min_value=1, 
            max_value=max(df['Complexity']), 
            value=10,
            help="Filter functions above this complexity threshold"
        )
        
        # Filter high complexity functions
        high_complexity = df[df['Complexity'] >= complexity_threshold]
        
        if not high_complexity.empty:
            st.write(f"**Functions with complexity >= {complexity_threshold}:**")
            st.dataframe(
                high_complexity[['File', 'Function', 'Complexity', 'LOC']].sort_values('Complexity', ascending=False),
                use_container_width=True
            )
        else:
            st.info(f"No functions found with complexity >= {complexity_threshold}")
    
    with col2:
        # Function complexity histogram
        fig = px.histogram(
            df, 
            x='Complexity', 
            nbins=20,
            title="Function Complexity Distribution",
            labels={'Complexity': 'Cyclomatic Complexity', 'count': 'Number of Functions'}
        )
        st.plotly_chart(fig, use_container_width=True)
      # Detailed function table
    st.subheader("📋 All Functions")
    
    # Sorting options
    sort_by = st.selectbox(
        "Sort by", 
        options=['Complexity', 'LOC', 'Nesting Depth', 'Parameters'],
        index=0
    )
    
    sorted_df = df.sort_values(sort_by, ascending=False)
    
    # Add complexity category for better visualization
    def get_complexity_category(complexity):
        if complexity >= 15:
            return "🔴 Very High"
        elif complexity >= 10:
            return "🟠 High"
        elif complexity >= 5:
            return "🟡 Medium"
        else:
            return "🟢 Low"
    
    # Add complexity category column
    display_df = sorted_df.copy()
    display_df['Complexity Level'] = display_df['Complexity'].apply(get_complexity_category)
    
    # Reorder columns for better display
    column_order = ['File', 'Function', 'Complexity', 'Complexity Level', 'LOC', 'Nesting Depth', 'Parameters']
    display_df = display_df[column_order]
    
    # Display the dataframe without styling issues
    st.dataframe(display_df, use_container_width=True)


def display_file_analysis(results: List[FileMetrics]):
    """Display file-level analysis"""
    
    st.subheader("📄 File Analysis")
    
    # File metrics table
    file_data = []
    for fm in results:
        avg_complexity = (sum(f.cyclomatic_complexity for f in fm.functions) / 
                         len(fm.functions)) if fm.functions else 0
        max_complexity = max((f.cyclomatic_complexity for f in fm.functions), default=0)
        
        file_data.append({
            'File': os.path.basename(fm.filepath),
            'LOC': fm.lines_of_code,
            'Functions': len(fm.functions),
            'Classes': len(fm.classes),
            'Avg Complexity': round(avg_complexity, 2),
            'Max Complexity': max_complexity,
            'Maintainability': round(fm.maintainability_index, 2),
            'Full Path': fm.filepath
        })
    
    df = pd.DataFrame(file_data)
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average File Size", f"{df['LOC'].mean():.0f} LOC")
    with col2:
        st.metric("Average Functions per File", f"{df['Functions'].mean():.1f}")
    with col3:
        st.metric("Files Needing Attention", len(df[df['Maintainability'] < 60]))
    
    # File details with recommendations
    for fm in results:
        with st.expander(f"📁 {os.path.basename(fm.filepath)} - Details"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Path:** `{fm.filepath}`")
                st.write(f"**Lines of Code:** {fm.lines_of_code}")
                st.write(f"**Functions:** {len(fm.functions)}")
                st.write(f"**Classes:** {len(fm.classes)}")
                st.write(f"**Maintainability Index:** {fm.maintainability_index:.1f}")
                
                # Quality assessment
                if fm.maintainability_index >= 80:
                    st.success("✅ Excellent maintainability")
                elif fm.maintainability_index >= 60:
                    st.warning("⚠️ Good maintainability")
                else:
                    st.error("❌ Poor maintainability - needs attention")
            
            with col2:
                if fm.functions:
                    # Function complexity chart for this file
                    func_complexities = [f.cyclomatic_complexity for f in fm.functions]
                    func_names = [f.name[:15] + '...' if len(f.name) > 15 else f.name 
                                 for f in fm.functions]
                    
                    fig = go.Figure(data=go.Bar(
                        x=func_names,
                        y=func_complexities,
                        marker_color=['red' if c >= 15 else 'orange' if c >= 10 else 'green' 
                                     for c in func_complexities]
                    ))
                    fig.update_layout(
                        title=f"Function Complexities",
                        xaxis_title="Functions",
                        yaxis_title="Complexity",
                        height=300
                    )
                    fig.update_xaxes(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)


def display_export_options(results: List[FileMetrics], summary: dict):
    """Display export options"""
    
    st.subheader("💾 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Export Formats Available:**")
        
        # JSON Export
        if st.button("📄 Export to JSON"):
            json_exporter = JsonExporter()
            json_data = json_exporter._prepare_data(results, summary)
            
            st.download_button(
                label="Download JSON",
                data=json_exporter._format_json(json_data),
                file_name="complexity_analysis.json",
                mime="application/json"
            )
        
        # CSV Export
        if st.button("📊 Export to CSV"):
            csv_exporter = CsvExporter()
            csv_data = csv_exporter._prepare_csv_data(results)
            
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="complexity_analysis.csv",
                mime="text/csv"
            )
    
    with col2:
        st.write("**Summary Report:**")
        
        # Display summary as formatted text
        summary_text = f"""
Code Complexity Analysis Report
===============================

Total Files: {summary['total_files']}
Total Functions: {summary['total_functions']}
Total Classes: {summary['total_classes']}
Total Lines of Code: {summary['total_loc']}

Average Complexity: {summary['average_complexity']:.2f}
Average Maintainability: {summary['average_maintainability']:.2f}
Quality Assessment: {summary['quality_assessment']}

Complexity Distribution:
"""
        
        for category, count in summary['complexity_distribution'].items():
            summary_text += f"  {category.replace('_', ' ').title()}: {count}\n"
        
        if summary['problematic_files']:
            summary_text += "\nFiles Needing Attention:\n"
            for pf in summary['problematic_files'][:5]:
                summary_text += f"  - {os.path.basename(pf['filepath'])} (MI: {pf['maintainability_index']:.1f})\n"
        
        st.text_area("Report Content", summary_text, height=300)
        
        st.download_button(
            label="Download Report",
            data=summary_text,
            file_name="complexity_report.txt",
            mime="text/plain"
        )


def get_quality_color(quality_assessment: str) -> str:
    """Get color for quality assessment"""
    colors = {
        "Excellent": "green",
        "Good": "blue",
        "Fair": "orange",
        "Needs Improvement": "red"
    }
    return colors.get(quality_assessment, "gray")


if __name__ == "__main__":
    main()
