"""
Visualization Module for Real Estate Price Prediction
Handles all plotting, charting, and visual analysis components
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
sns.set_palette("husl")

class RealEstateVisualizer:
    def __init__(self, figsize=(12, 8)):
        self.figsize = figsize
        self.color_palette = sns.color_palette("husl", 10)
        
    def plot_price_distribution(self, df: pd.DataFrame, column='price'):
        """Plot price distribution with statistics"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Property Price Distribution Analysis', fontsize=16, fontweight='bold')
        
        # Histogram
        axes[0, 0].hist(df[column], bins=50, alpha=0.7, color=self.color_palette[0], edgecolor='black')
        axes[0, 0].set_title('Price Distribution')
        axes[0, 0].set_xlabel('Price ($)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].axvline(df[column].mean(), color='red', linestyle='--', label=f'Mean: ${df[column].mean():,.0f}')
        axes[0, 0].axvline(df[column].median(), color='green', linestyle='--', label=f'Median: ${df[column].median():,.0f}')
        axes[0, 0].legend()
        
        # Box plot
        axes[0, 1].boxplot(df[column])
        axes[0, 1].set_title('Price Box Plot')
        axes[0, 1].set_ylabel('Price ($)')
        
        # Log-scale histogram
        axes[1, 0].hist(np.log10(df[column]), bins=50, alpha=0.7, color=self.color_palette[1], edgecolor='black')
        axes[1, 0].set_title('Price Distribution (Log Scale)')
        axes[1, 0].set_xlabel('Log10(Price)')
        axes[1, 0].set_ylabel('Frequency')
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(df[column], dist="norm", plot=axes[1, 1])
        axes[1, 1].set_title('Q-Q Plot (Normal Distribution)')
        
        plt.tight_layout()
        return fig
    
    def plot_correlation_matrix(self, df: pd.DataFrame, figsize=(12, 10)):
        """Plot correlation matrix heatmap"""
        # Select only numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        plt.figure(figsize=figsize)
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        sns.heatmap(correlation_matrix, 
                   mask=mask,
                   annot=True, 
                   cmap='coolwarm', 
                   center=0,
                   square=True,
                   fmt='.2f',
                   cbar_kws={"shrink": .8})
        
        plt.title('Feature Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return plt.gcf()
    
    def plot_feature_importance(self, importance_df: pd.DataFrame, top_n=20):
        """Plot feature importance"""
        top_features = importance_df.head(top_n)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        
        # Horizontal bar plot
        bars = ax1.barh(range(len(top_features)), top_features['importance'])
        ax1.set_yticks(range(len(top_features)))
        ax1.set_yticklabels(top_features['feature'])
        ax1.set_xlabel('Importance')
        ax1.set_title(f'Top {top_n} Feature Importances')
        ax1.invert_yaxis()
        
        # Color bars by importance
        for i, bar in enumerate(bars):
            bar.set_color(plt.cm.viridis(top_features.iloc[i]['importance'] / top_features['importance'].max()))
        
        # Pie chart for top 10
        top_10 = top_features.head(10)
        ax2.pie(top_10['importance'], labels=top_10['feature'], autopct='%1.1f%%', startangle=90)
        ax2.set_title('Top 10 Features Distribution')
        
        plt.tight_layout()
        return fig
    
    def plot_price_by_categorical(self, df: pd.DataFrame, categorical_columns: List[str]):
        """Plot price distribution by categorical variables"""
        n_cols = len(categorical_columns)
        n_rows = (n_cols + 1) // 2
        
        fig, axes = plt.subplots(n_rows, 2, figsize=(15, 5*n_rows))
        if n_rows == 1:
            axes = [axes]
        
        for i, col in enumerate(categorical_columns):
            row = i // 2
            col_idx = i % 2
            
            if n_rows > 1:
                ax = axes[row][col_idx]
            else:
                ax = axes[col_idx]
            
            # Box plot
            df.boxplot(column='price', by=col, ax=ax)
            ax.set_title(f'Price Distribution by {col}')
            ax.set_xlabel(col)
            ax.set_ylabel('Price ($)')
            plt.setp(ax.get_xticklabels(), rotation=45)
        
        # Remove empty subplot if odd number of columns
        if n_cols % 2 == 1 and n_rows > 1:
            fig.delaxes(axes[n_rows-1][1])
        
        plt.suptitle('Price Distribution by Categorical Variables', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_geographic_analysis(self, df: pd.DataFrame):
        """Plot geographic price analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Price by coordinates scatter plot
        scatter = axes[0, 0].scatter(df['longitude'], df['latitude'], 
                                   c=df['price'], cmap='viridis', alpha=0.6, s=30)
        axes[0, 0].set_xlabel('Longitude')
        axes[0, 0].set_ylabel('Latitude')
        axes[0, 0].set_title('Price Distribution by Location')
        plt.colorbar(scatter, ax=axes[0, 0], label='Price ($)')
        
        # Average price by neighborhood
        if 'neighborhood' in df.columns:
            neighborhood_price = df.groupby('neighborhood')['price'].mean().sort_values(ascending=True)
            axes[0, 1].barh(range(len(neighborhood_price)), neighborhood_price.values)
            axes[0, 1].set_yticks(range(len(neighborhood_price)))
            axes[0, 1].set_yticklabels(neighborhood_price.index)
            axes[0, 1].set_xlabel('Average Price ($)')
            axes[0, 1].set_title('Average Price by Neighborhood')
        
        # Distance from center vs price
        if 'distance_from_center' in df.columns:
            axes[1, 0].scatter(df['distance_from_center'], df['price'], alpha=0.6)
            axes[1, 0].set_xlabel('Distance from Center (km)')
            axes[1, 0].set_ylabel('Price ($)')
            axes[1, 0].set_title('Price vs Distance from Center')
            
            # Add trend line
            z = np.polyfit(df['distance_from_center'], df['price'], 1)
            p = np.poly1d(z)
            axes[1, 0].plot(df['distance_from_center'], p(df['distance_from_center']), "r--", alpha=0.8)
        
        # Walkability score vs price
        if 'walkability_score' in df.columns:
            axes[1, 1].scatter(df['walkability_score'], df['price'], alpha=0.6)
            axes[1, 1].set_xlabel('Walkability Score')
            axes[1, 1].set_ylabel('Price ($)')
            axes[1, 1].set_title('Price vs Walkability Score')
            
            # Add trend line
            z = np.polyfit(df['walkability_score'], df['price'], 1)
            p = np.poly1d(z)
            axes[1, 1].plot(df['walkability_score'], p(df['walkability_score']), "r--", alpha=0.8)
        
        plt.tight_layout()
        return fig
    
    def plot_model_performance(self, performance_df: pd.DataFrame):
        """Plot model performance comparison"""
        metrics = ['R2', 'RMSE', 'MAE', 'MAPE']
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, metric in enumerate(metrics):
            if metric in performance_df.columns:
                bars = axes[i].bar(performance_df.index, performance_df[metric])
                axes[i].set_title(f'{metric} by Model')
                axes[i].set_ylabel(metric)
                plt.setp(axes[i].get_xticklabels(), rotation=45)
                
                # Color bars
                for j, bar in enumerate(bars):
                    if metric in ['R2']:  # Higher is better
                        bar.set_color(plt.cm.viridis(performance_df[metric].iloc[j] / performance_df[metric].max()))
                    else:  # Lower is better
                        bar.set_color(plt.cm.viridis_r(performance_df[metric].iloc[j] / performance_df[metric].max()))
        
        plt.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_prediction_analysis(self, y_true: np.ndarray, y_pred: np.ndarray, model_name: str = "Model"):
        """Plot prediction vs actual analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Prediction vs Actual scatter plot
        axes[0, 0].scatter(y_true, y_pred, alpha=0.6)
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        axes[0, 0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        axes[0, 0].set_xlabel('Actual Price ($)')
        axes[0, 0].set_ylabel('Predicted Price ($)')
        axes[0, 0].set_title(f'{model_name}: Predicted vs Actual')
        
        # Residuals plot
        residuals = y_pred - y_true
        axes[0, 1].scatter(y_pred, residuals, alpha=0.6)
        axes[0, 1].axhline(y=0, color='r', linestyle='--')
        axes[0, 1].set_xlabel('Predicted Price ($)')
        axes[0, 1].set_ylabel('Residuals ($)')
        axes[0, 1].set_title('Residuals Plot')
        
        # Residuals histogram
        axes[1, 0].hist(residuals, bins=50, alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('Residuals ($)')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Residuals Distribution')
        
        # Percentage error distribution
        percentage_error = (residuals / y_true) * 100
        axes[1, 1].hist(percentage_error, bins=50, alpha=0.7, edgecolor='black')
        axes[1, 1].set_xlabel('Percentage Error (%)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Percentage Error Distribution')
        axes[1, 1].axvline(percentage_error.mean(), color='red', linestyle='--', 
                          label=f'Mean: {percentage_error.mean():.1f}%')
        axes[1, 1].legend()
        
        plt.suptitle(f'{model_name} - Prediction Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def plot_poi_analysis(self, df: pd.DataFrame):
        """Plot POI (Points of Interest) analysis"""
        poi_columns = [col for col in df.columns if col.startswith('distance_to_')]
        
        if not poi_columns:
            print("No POI distance columns found.")
            return None
        
        n_pois = len(poi_columns)
        n_rows = (n_pois + 1) // 2
        
        fig, axes = plt.subplots(n_rows, 2, figsize=(15, 5*n_rows))
        if n_rows == 1:
            axes = [axes]
        
        for i, col in enumerate(poi_columns):
            row = i // 2
            col_idx = i % 2
            
            if n_rows > 1:
                ax = axes[row][col_idx]
            else:
                ax = axes[col_idx]
            
            # Scatter plot of distance vs price
            ax.scatter(df[col], df['price'], alpha=0.6)
            ax.set_xlabel(f'Distance to {col.replace("distance_to_", "").replace("_", " ").title()} (km)')
            ax.set_ylabel('Price ($)')
            ax.set_title(f'Price vs {col.replace("distance_to_", "").replace("_", " ").title()} Distance')
            
            # Add correlation coefficient
            corr = df[col].corr(df['price'])
            ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=ax.transAxes, 
                   bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.5))
        
        # Remove empty subplot if odd number of POIs
        if n_pois % 2 == 1 and n_rows > 1:
            fig.delaxes(axes[n_rows-1][1])
        
        plt.suptitle('POI Distance Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
    
    def create_interactive_price_scatter(self, df: pd.DataFrame):
        """Create interactive scatter plot with Plotly"""
        fig = px.scatter(
            df, 
            x='square_feet', 
            y='price',
            color='neighborhood' if 'neighborhood' in df.columns else None,
            size='bedrooms' if 'bedrooms' in df.columns else None,
            hover_data=['bathrooms', 'property_type'] if all(col in df.columns for col in ['bathrooms', 'property_type']) else None,
            title='Interactive Property Price Analysis',
            labels={'square_feet': 'Square Feet', 'price': 'Price ($)'}
        )
        
        fig.update_layout(
            width=800,
            height=600,
            showlegend=True
        )
        
        return fig
    
    def create_dashboard_summary(self, df: pd.DataFrame, performance_df: pd.DataFrame = None):
        """Create a comprehensive dashboard summary"""
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=[
                'Price Distribution', 'Property Types', 'Bedrooms vs Price',
                'Price by Neighborhood', 'Square Feet vs Price', 'Property Age vs Price',
                'Model Performance (R²)', 'Geographic Distribution', 'Feature Correlations'
            ],
            specs=[
                [{"type": "histogram"}, {"type": "pie"}, {"type": "box"}],
                [{"type": "bar"}, {"type": "scatter"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "scatter"}, {"type": "scatter"}]
            ]
        )
        
        # Price distribution
        fig.add_trace(
            go.Histogram(x=df['price'], nbinsx=30, name='Price Distribution'),
            row=1, col=1
        )
        
        # Property types
        if 'property_type' in df.columns:
            type_counts = df['property_type'].value_counts()
            fig.add_trace(
                go.Pie(labels=type_counts.index, values=type_counts.values, name='Property Types'),
                row=1, col=2
            )
        
        # Bedrooms vs Price
        if 'bedrooms' in df.columns:
            fig.add_trace(
                go.Box(x=df['bedrooms'], y=df['price'], name='Bedrooms vs Price'),
                row=1, col=3
            )
        
        # Price by neighborhood
        if 'neighborhood' in df.columns:
            neighborhood_avg = df.groupby('neighborhood')['price'].mean()
            fig.add_trace(
                go.Bar(x=neighborhood_avg.index, y=neighborhood_avg.values, name='Avg Price by Neighborhood'),
                row=2, col=1
            )
        
        # Square feet vs Price
        if 'square_feet' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['square_feet'], y=df['price'], mode='markers', name='Size vs Price'),
                row=2, col=2
            )
        
        # Property age vs Price
        if 'property_age' in df.columns:
            fig.add_trace(
                go.Scatter(x=df['property_age'], y=df['price'], mode='markers', name='Age vs Price'),
                row=2, col=3
            )
        
        # Model performance
        if performance_df is not None and 'R2' in performance_df.columns:
            fig.add_trace(
                go.Bar(x=performance_df.index, y=performance_df['R2'], name='Model R² Score'),
                row=3, col=1
            )
        
        # Geographic distribution
        if all(col in df.columns for col in ['latitude', 'longitude']):
            fig.add_trace(
                go.Scatter(x=df['longitude'], y=df['latitude'], mode='markers', 
                          marker=dict(color=df['price'], colorscale='Viridis'),
                          name='Geographic Distribution'),
                row=3, col=2
            )
        
        # Feature correlations (example with key features)
        key_features = ['bedrooms', 'bathrooms', 'square_feet']
        available_features = [f for f in key_features if f in df.columns]
        if available_features:
            correlations = [df[feature].corr(df['price']) for feature in available_features]
            fig.add_trace(
                go.Scatter(x=available_features, y=correlations, mode='markers+lines', name='Price Correlations'),
                row=3, col=3
            )
        
        fig.update_layout(
            height=1200,
            title_text="Real Estate Analysis Dashboard",
            showlegend=False
        )
        
        return fig
    
    def plot_text_analysis(self, df: pd.DataFrame):
        """Plot NLP text analysis results"""
        text_features = [col for col in df.columns if any(x in col for x in [
            'sentiment_', 'description_length', 'word_count', 'positive_keyword_count', 
            'luxury_keyword_count'
        ])]
        
        if not text_features:
            print("No text analysis features found.")
            return None
        
        n_features = min(6, len(text_features))  # Limit to 6 features for visualization
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        axes = axes.flatten()
        
        for i, feature in enumerate(text_features[:n_features]):
            ax = axes[i]
            
            if 'sentiment_' in feature and feature != 'sentiment_compound':
                # Bar plot for sentiment categories
                sentiment_mean = df.groupby('neighborhood')[feature].mean() if 'neighborhood' in df.columns else df[feature].mean()
                if hasattr(sentiment_mean, 'plot'):
                    sentiment_mean.plot(kind='bar', ax=ax)
                else:
                    ax.bar(['Overall'], [sentiment_mean])
                ax.set_title(f'{feature.replace("_", " ").title()}')
                ax.set_ylabel('Score')
            else:
                # Scatter plot vs price
                ax.scatter(df[feature], df['price'], alpha=0.6)
                ax.set_xlabel(feature.replace('_', ' ').title())
                ax.set_ylabel('Price ($)')
                ax.set_title(f'Price vs {feature.replace("_", " ").title()}')
                
                # Add correlation
                corr = df[feature].corr(df['price'])
                ax.text(0.05, 0.95, f'Corr: {corr:.3f}', transform=ax.transAxes,
                       bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.5))
        
        # Hide unused subplots
        for j in range(n_features, 6):
            axes[j].set_visible(False)
        
        plt.suptitle('Text Analysis Impact on Price', fontsize=16, fontweight='bold')
        plt.tight_layout()
        return fig
