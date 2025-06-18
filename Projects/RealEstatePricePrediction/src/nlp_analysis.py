"""
NLP Analysis Module for Real Estate Property Descriptions
Handles sentiment analysis, keyword extraction, and text feature engineering
"""

import pandas as pd
import numpy as np
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Text processing libraries
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import WordNetLemmatizer
    from nltk.sentiment import SentimentIntensityAnalyzer
    
    # Download required NLTK data
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans

class PropertyDescriptionAnalyzer:
    def __init__(self):
        self.stop_words = set()
        self.lemmatizer = None
        self.sentiment_analyzer = None
        self.tfidf_vectorizer = None
        self.feature_names = []
        
        if NLTK_AVAILABLE:
            self.stop_words = set(stopwords.words('english'))
            self.lemmatizer = WordNetLemmatizer()
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Real estate specific keywords
        self.positive_keywords = [
            'beautiful', 'stunning', 'gorgeous', 'spacious', 'modern', 'updated',
            'renovated', 'luxury', 'premium', 'excellent', 'perfect', 'amazing',
            'spectacular', 'pristine', 'immaculate', 'charming', 'elegant',
            'contemporary', 'stylish', 'desirable', 'prime', 'convenient'
        ]
        
        self.negative_keywords = [
            'outdated', 'old', 'needs work', 'fixer', 'dated', 'worn',
            'repair needed', 'renovation required', 'compact', 'cozy',
            'intimate', 'starter', 'investment opportunity'
        ]
        
        self.luxury_keywords = [
            'luxury', 'premium', 'high-end', 'upscale', 'exclusive', 'elite',
            'prestigious', 'gourmet', 'master suite', 'walk-in closet',
            'marble', 'granite', 'stainless steel', 'hardwood', 'cathedral',
            'vaulted', 'crown molding', 'fireplace', 'pool', 'spa'
        ]
        
        self.location_keywords = [
            'waterfront', 'ocean view', 'mountain view', 'city view', 'quiet',
            'peaceful', 'central', 'downtown', 'suburban', 'rural', 'urban',
            'walkable', 'transportation', 'schools', 'shopping', 'dining'
        ]
    
    def clean_text(self, text):
        """Clean and preprocess text"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_keywords(self, text, keyword_list):
        """Extract specific keywords from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_keywords = [keyword for keyword in keyword_list if keyword in text_lower]
        return found_keywords
    
    def calculate_sentiment_scores(self, df):
        """Calculate sentiment scores for property descriptions"""
        print("Calculating sentiment scores...")
        
        sentiments = []
        
        for idx, description in df['description'].iterrows() if hasattr(df['description'], 'iterrows') else enumerate(df['description']):
            if pd.isna(description) or description == "":
                sentiment_score = {
                    'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1,
                    'textblob_polarity': 0, 'textblob_subjectivity': 0
                }
            else:
                # NLTK VADER sentiment
                if NLTK_AVAILABLE and self.sentiment_analyzer:
                    vader_scores = self.sentiment_analyzer.polarity_scores(description)
                    sentiment_score = vader_scores.copy()
                else:
                    sentiment_score = {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1}
                
                # TextBlob sentiment
                if TEXTBLOB_AVAILABLE:
                    blob = TextBlob(description)
                    sentiment_score['textblob_polarity'] = blob.sentiment.polarity
                    sentiment_score['textblob_subjectivity'] = blob.sentiment.subjectivity
                else:
                    sentiment_score['textblob_polarity'] = 0
                    sentiment_score['textblob_subjectivity'] = 0
            
            sentiments.append(sentiment_score)
        
        # Convert to DataFrame
        sentiment_df = pd.DataFrame(sentiments)
        
        # Add sentiment columns to original dataframe
        for col in sentiment_df.columns:
            df[f'sentiment_{col}'] = sentiment_df[col].values
        
        print("Sentiment analysis completed.")
        return df
    
    def extract_description_features(self, df):
        """Extract various features from property descriptions"""
        print("Extracting description features...")
        
        # Initialize feature columns
        df['description_length'] = 0
        df['word_count'] = 0
        df['sentence_count'] = 0
        df['positive_keyword_count'] = 0
        df['negative_keyword_count'] = 0
        df['luxury_keyword_count'] = 0
        df['location_keyword_count'] = 0
        df['exclamation_count'] = 0
        df['capital_ratio'] = 0
        
        for idx, row in df.iterrows():
            description = row.get('description', '')
            if pd.isna(description):
                description = ''
            
            original_desc = str(description)
            clean_desc = self.clean_text(description)
            
            # Basic text statistics
            df.loc[idx, 'description_length'] = len(original_desc)
            df.loc[idx, 'word_count'] = len(clean_desc.split()) if clean_desc else 0
            df.loc[idx, 'exclamation_count'] = original_desc.count('!')
            
            # Capital letter ratio
            if len(original_desc) > 0:
                df.loc[idx, 'capital_ratio'] = sum(1 for c in original_desc if c.isupper()) / len(original_desc)
            
            # Sentence count
            if NLTK_AVAILABLE:
                df.loc[idx, 'sentence_count'] = len(sent_tokenize(original_desc))
            else:
                df.loc[idx, 'sentence_count'] = original_desc.count('.') + original_desc.count('!') + original_desc.count('?')
            
            # Keyword counts
            df.loc[idx, 'positive_keyword_count'] = len(self.extract_keywords(clean_desc, self.positive_keywords))
            df.loc[idx, 'negative_keyword_count'] = len(self.extract_keywords(clean_desc, self.negative_keywords))
            df.loc[idx, 'luxury_keyword_count'] = len(self.extract_keywords(clean_desc, self.luxury_keywords))
            df.loc[idx, 'location_keyword_count'] = len(self.extract_keywords(clean_desc, self.location_keywords))
        
        # Create derived features
        df['positive_negative_ratio'] = df['positive_keyword_count'] / (df['negative_keyword_count'] + 1)
        df['luxury_score_text'] = df['luxury_keyword_count'] / (df['word_count'] + 1)
        df['description_quality_score'] = (
            df['positive_keyword_count'] * 2 + 
            df['luxury_keyword_count'] * 3 - 
            df['negative_keyword_count'] +
            (df['word_count'] > 20).astype(int) * 2
        )
        
        print("Description features extracted.")
        return df
    
    def create_tfidf_features(self, df, max_features=50):
        """Create TF-IDF features from descriptions"""
        print(f"Creating TF-IDF features (max {max_features} features)...")
        
        # Clean descriptions
        descriptions = df['description'].fillna('').apply(self.clean_text)
        
        # Remove empty descriptions
        non_empty_descriptions = descriptions[descriptions != '']
        
        if len(non_empty_descriptions) == 0:
            print("No non-empty descriptions found.")
            return df
        
        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            min_df=2,  # Minimum document frequency
            max_df=0.8  # Maximum document frequency
        )
        
        # Fit and transform
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(descriptions)
            self.feature_names = self.tfidf_vectorizer.get_feature_names_out()
            
            # Convert to DataFrame
            tfidf_df = pd.DataFrame(
                tfidf_matrix.toarray(),
                columns=[f'tfidf_{name}' for name in self.feature_names],
                index=df.index
            )
            
            # Merge with original DataFrame
            df = pd.concat([df, tfidf_df], axis=1)
            
            print(f"TF-IDF features created: {len(self.feature_names)} features")
            
        except Exception as e:
            print(f"Error creating TF-IDF features: {e}")
        
        return df
    
    def cluster_descriptions(self, df, n_clusters=5):
        """Cluster property descriptions using TF-IDF features"""
        print(f"Clustering descriptions into {n_clusters} clusters...")
        
        # Get TF-IDF columns
        tfidf_columns = [col for col in df.columns if col.startswith('tfidf_')]
        
        if not tfidf_columns:
            print("No TF-IDF features found. Please run create_tfidf_features first.")
            return df
        
        # Perform clustering
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            df['description_cluster'] = kmeans.fit_predict(df[tfidf_columns])
            
            # Analyze clusters
            cluster_analysis = self.analyze_description_clusters(df, tfidf_columns)
            
            print("Description clustering completed.")
            return df, cluster_analysis
            
        except Exception as e:
            print(f"Error in clustering: {e}")
            return df, None
    
    def analyze_description_clusters(self, df, tfidf_columns):
        """Analyze the characteristics of description clusters"""
        cluster_analysis = {}
        
        for cluster_id in df['description_cluster'].unique():
            cluster_data = df[df['description_cluster'] == cluster_id]
            
            # Get top TF-IDF features for this cluster
            cluster_tfidf_means = cluster_data[tfidf_columns].mean()
            top_features = cluster_tfidf_means.nlargest(10)
            
            # Calculate cluster statistics
            analysis = {
                'size': len(cluster_data),
                'avg_price': cluster_data['price'].mean(),
                'avg_description_length': cluster_data['description_length'].mean(),
                'avg_positive_keywords': cluster_data['positive_keyword_count'].mean(),
                'avg_luxury_keywords': cluster_data['luxury_keyword_count'].mean(),
                'top_tfidf_features': top_features.to_dict(),
                'sample_descriptions': cluster_data['description'].head(3).tolist()
            }
            
            cluster_analysis[f'Cluster_{cluster_id}'] = analysis
        
        return cluster_analysis
    
    def generate_word_cloud(self, df, column='description'):
        """Generate word cloud from property descriptions"""
        if not WORDCLOUD_AVAILABLE:
            print("WordCloud not available. Install with: pip install wordcloud")
            return None
        
        # Combine all descriptions
        all_text = ' '.join(df[column].fillna('').astype(str))
        all_text = self.clean_text(all_text)
        
        if not all_text.strip():
            print("No text available for word cloud.")
            return None
        
        # Create word cloud
        try:
            wordcloud = WordCloud(
                width=800, 
                height=400, 
                background_color='white',
                stopwords=self.stop_words,
                max_words=100,
                colormap='viridis'
            ).generate(all_text)
            
            return wordcloud
            
        except Exception as e:
            print(f"Error generating word cloud: {e}")
            return None
    
    def extract_property_features_from_text(self, df):
        """Extract property features mentioned in descriptions"""
        print("Extracting property features from text...")
        
        # Feature keywords to look for
        feature_keywords = {
            'has_fireplace_text': ['fireplace', 'fire place'],
            'has_pool_text': ['pool', 'swimming'],
            'has_garage_text': ['garage', 'parking', 'carport'],
            'has_garden_text': ['garden', 'yard', 'landscaping'],
            'has_balcony_text': ['balcony', 'terrace', 'deck', 'patio'],
            'has_basement_text': ['basement', 'lower level'],
            'has_attic_text': ['attic', 'loft'],
            'has_hardwood_text': ['hardwood', 'wood floor'],
            'has_granite_text': ['granite', 'quartz countertop'],
            'has_stainless_text': ['stainless steel', 'stainless appliances'],
            'recently_updated_text': ['updated', 'renovated', 'remodeled', 'new'],
            'move_in_ready_text': ['move-in ready', 'turnkey', 'ready to move']
        }
        
        for feature_name, keywords in feature_keywords.items():
            df[feature_name] = 0
            for idx, description in enumerate(df['description']):
                if pd.isna(description):
                    continue
                description_lower = str(description).lower()
                if any(keyword in description_lower for keyword in keywords):
                    df.loc[idx, feature_name] = 1
        
        print("Property features extracted from text.")
        return df
    
    def comprehensive_text_analysis(self, df):
        """Perform comprehensive text analysis pipeline"""
        print("Starting comprehensive NLP analysis...")
        
        # Calculate sentiment scores
        df = self.calculate_sentiment_scores(df)
        
        # Extract description features
        df = self.extract_description_features(df)
        
        # Extract property features from text
        df = self.extract_property_features_from_text(df)
        
        # Create TF-IDF features
        df = self.create_tfidf_features(df)
        
        # Cluster descriptions
        df, cluster_analysis = self.cluster_descriptions(df)
        
        print("Comprehensive NLP analysis completed.")
        return df, cluster_analysis
    
    def get_text_feature_importance(self, df, target_column='price'):
        """Calculate correlation between text features and target variable"""
        text_columns = [col for col in df.columns if any(x in col for x in [
            'sentiment_', 'description_', 'positive_', 'negative_', 'luxury_',
            'location_', 'tfidf_', 'has_', 'recently_', 'move_in_'
        ])]
        
        correlations = []
        for col in text_columns:
            if col in df.columns and target_column in df.columns:
                corr = df[col].corr(df[target_column])
                if not pd.isna(corr):
                    correlations.append({
                        'feature': col,
                        'correlation': corr,
                        'abs_correlation': abs(corr)
                    })
        
        correlation_df = pd.DataFrame(correlations)
        correlation_df = correlation_df.sort_values('abs_correlation', ascending=False)
        
        return correlation_df
