import re
import json
import time

def extract_ml_category_only():
    """
    Extract ONLY the Machine Learning category questions (63 total)
    """
    print("Extracting ONLY Machine Learning Category questions...")
    print("=" * 100)
    
    html_file = 'D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\debug_page.html'
    
    try:
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("✓ HTML file loaded")
        
        # Find the Machine Learning topic data structure
        # Looking for: const topics = [...] or similar JavaScript array
        
        # Search for the ML topic definition
        ml_topic_pattern = r"(?:topic|name):\s*['\"](?:🤖\s*)?Machine Learning['\"].*?questions:\s*\[(.*?)\]"
        ml_match = re.search(ml_topic_pattern, html_content, re.DOTALL | re.IGNORECASE)
        
        if not ml_match:
            # Try alternative pattern - look for ML questions array
            print("  Trying alternative pattern...")
            
            # Find all topics and filter for Machine Learning
            # Pattern: Look for topic objects with icon 🤖
            topics_pattern = r"topics\s*=\s*\[(.*?)\];\s*(?:const|let|var)"
            topics_match = re.search(topics_pattern, html_content, re.DOTALL)
            
            if topics_match:
                topics_data = topics_match.group(1)
                # Find the ML topic within topics
                ml_in_topics = re.search(r"\{[^}]*?(?:icon|name):\s*['\"]🤖['\"].*?\[(.*?)\].*?\}", topics_data, re.DOTALL)
                if ml_in_topics:
                    ml_questions_str = ml_in_topics.group(1)
                else:
                    print("  Could not find ML topic, extracting by filtering...")
                    ml_questions_str = None
            else:
                ml_questions_str = None
        else:
            ml_questions_str = ml_match.group(1)
        
        # Extract all questions and filter by known ML questions
        pattern = r"\{q:'([^']+(?:\\'[^']*)*)',a:'([^']+(?:\\'[^']*)*)'(?:,difficulty:'([^']*)')?(?:,tags:\[([^\]]*)\])?(?:,companies:\[([^\]]*)\])?\}"
        
        all_matches = re.findall(pattern, html_content, re.DOTALL)
        print(f"✓ Found {len(all_matches)} total question objects")
        
        # Known ML category question starters from the user's list
        ml_question_keywords = [
            "Walk through building an end-to-end churn prediction model",
            "Explain bias-variance tradeoff",
            "How does XGBoost handle missing values",
            "When choose LR over neural network",
            "95% accuracy but stakeholder unhappy",
            "SHAP vs RF feature importance",
            "What is data leakage",
            "L1 vs L2 regularization",
            "Detect and handle multicollinearity",
            "Gradient descent variants",
            "Cross-validation types",
            "Random Forest advantages",
            "XGBoost vs vanilla gradient boosting",
            "Handle highly imbalanced dataset",
            "Curse of dimensionality",
            "Explain PCA",
            "ROC curve and AUC",
            "K-means",
            "Transfer learning",
            "Feature selection methods",
            "Generative vs discriminative",
            "SVM explained",
            "EM algorithm",
            "Naive Bayes",
            "Decision tree splitting",
            "Dropout",
            "Batch normalization",
            "Vanishing/exploding gradient",
            "Bagging vs boosting",
            "Evaluate regression model",
            "Transformer architecture",
            "Word2Vec",
            "CNN key components",
            "LSTM",
            "Learning rate",
            "Early stopping",
            "KNN pros and cons",
            "GAN",
            "VAE vs GAN",
            "Model calibration",
            "contrastive learning",
            "Federated learning",
            "Few-shot learning",
            "Model pruning",
            "Quantization in ML",
            "Mixture of Experts",
            "Gaussian Process",
            "Lottery Ticket Hypothesis",
            "Knowledge distillation",
            "curriculum learning",
            "Active learning",
            "high-cardinality categoricals",
            "Loss functions",
            "Label smoothing",
            "Catastrophic forgetting",
            "Zero-shot learning",
            "Online vs batch learning",
            "confusion matrix",
            "Parametric vs non-parametric",
            "Semi-supervised learning",
            "Attention mechanism",
            "model interpretability vs explainability",
            "multi-task learning"
        ]
        
        ml_questions = []
        
        for match in all_matches:
            q_text = match[0].replace("\\'", "'").replace("\\n", "\n")
            a_text = match[1].replace("\\'", "'").replace("\\n", "\n") if match[1] else ""
            difficulty = match[2] if len(match) > 2 else ""
            tags = match[3] if len(match) > 3 else ""
            companies = match[4] if len(match) > 4 else ""
            
            # Check if this is an ML category question
            is_ml_category = any(keyword.lower() in q_text.lower() for keyword in ml_question_keywords)
            
            # Also check tags for ML-specific tags (not stats/probability)
            ml_specific_tags = ['XGBoost', 'System Design', 'Model Selection', 'Imbalanced Data', 
                               'Explainability', 'Best Practices', 'Regularization', 'Regression',
                               'Optimization', 'Validation', 'Ensembles', 'Boosting', 'Dimensionality',
                               'PCA', 'Evaluation', 'Clustering', 'Transfer Learning', 'Feature Selection',
                               'Model Types', 'SVM', 'Classification', 'Trees', 'Deep Learning', 'NLP',
                               'CNN', 'RNN', 'Generative Models', 'Calibration', 'Self-supervised',
                               'Privacy', 'Meta-learning', 'Compression', 'Deployment', 'Architecture',
                               'Bayesian', 'Theory', 'Training', 'Data Efficiency', 'Feature Engineering',
                               'Continual Learning', 'Learning Paradigms', 'Ethics']
            
            has_ml_tag = any(tag in tags for tag in ml_specific_tags)
            
            # Exclude stats/probability questions
            stats_keywords = ['p-value', 'confidence interval', 'hypothesis test', 'bayes theorem',
                            'central limit', 'LLN', 'CLT', 'disease', 'coin', 'birthday problem',
                            'A/B test', 'Simpson', 'MLE', 'sufficient statistic', 'kaplan-meier',
                            'bootstrapping', 'power', 'sample size']
            is_stats = any(keyword.lower() in q_text.lower() for keyword in stats_keywords)
            
            if (is_ml_category or has_ml_tag) and not is_stats:
                ml_questions.append({
                    'question': q_text,
                    'answer': a_text,
                    'difficulty': difficulty,
                    'tags': tags,
                    'companies': companies
                })
        
        print(f"✓ Filtered to {len(ml_questions)} Machine Learning category questions")
        
        # Write to output file
        output_path = 'D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\scrapper_output.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("🤖 MACHINE LEARNING - INTERVIEW QUESTIONS FOR ML ENGINEER\n")
            f.write("=" * 100 + "\n")
            f.write("Scraped from: https://cracked-ds-platform.vercel.app/\n")
            f.write("Role: ML Engineer (⚙️)\n")
            f.write("Category: 🤖 Machine Learning ONLY\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Questions: {len(ml_questions)}\n")
            f.write("=" * 100 + "\n\n")
            
            for idx, qa in enumerate(ml_questions, 1):
                f.write(f"\n{'=' * 100}\n")
                f.write(f"QUESTION {idx}")
                if qa['difficulty']:
                    f.write(f" [{qa['difficulty']}]")
                f.write("\n")
                f.write(f"{'=' * 100}\n\n")
                
                f.write(f"{qa['question']}\n\n")
                
                f.write(f"{'-' * 100}\n")
                f.write(f"ANSWER:\n")
                f.write(f"{'-' * 100}\n\n")
                
                if qa['answer']:
                    f.write(f"{qa['answer']}\n\n")
                else:
                    f.write("[No answer provided]\n\n")
                
                # Add metadata
                if qa['tags']:
                    f.write(f"📌 Tags: {qa['tags']}\n")
                if qa['companies']:
                    f.write(f"🏢 Companies: {qa['companies']}\n")
                
                f.write("\n")
        
        print(f"\n✓ SUCCESS!")
        print(f"  Machine Learning questions saved to: scrapper_output.txt")
        print(f"  Total questions: {len(ml_questions)}")
        
        return ml_questions
        
    except FileNotFoundError:
        print(f"✗ ERROR: Could not find {html_file}")
        return []
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    questions = extract_ml_category_only()
    print("\n" + "=" * 100)
    print("EXTRACTION COMPLETED!")
    print("=" * 100)
