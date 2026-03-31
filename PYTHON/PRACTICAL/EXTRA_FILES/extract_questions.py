import re
import json
from bs4 import BeautifulSoup
import time

def extract_ml_questions_from_html():
    """
    Extract Machine Learning questions from the saved debug HTML file
    """
    print("Extracting ML Engineer - Machine Learning questions from debug HTML...")
    print("=" * 100)
    
    html_file = 'D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\debug_page.html'
    
    try:
        # Read the HTML file
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print("✓ HTML file loaded")
        
        # Find all question objects in the JavaScript code
        # Pattern: {q:'...',a:'...',difficulty:'...',tags:[...],companies:[...]}
        pattern = r"\{q:'([^']+(?:\\'[^']*)*)',a:'([^']+(?:\\'[^']*)*)'(?:,difficulty:'([^']*)')?(?:,tags:\[([^\]]*)\])?(?:,companies:\[([^\]]*)\])?\}"
        
        matches = re.findall(pattern, html_content, re.DOTALL)
        
        print(f"✓ Found {len(matches)} question objects")
        
        questions = []
        for match in matches:
            q_text = match[0].replace("\\'", "'").replace("\\n", "\n")
            a_text = match[1].replace("\\'", "'").replace("\\n", "\n") if match[1] else ""
            difficulty = match[2] if len(match) > 2 else ""
            tags = match[3] if len(match) > 3 else ""
            companies = match[4] if len(match) > 4 else ""
            
            questions.append({
                'question': q_text,
                'answer': a_text,
                'difficulty': difficulty,
                'tags': tags,
                'companies': companies
            })
        
        # Filter for Machine Learning questions (based on tags or content)
        ml_questions = []
        for q in questions:
            # Check if it's an ML-related question
            tags_lower = q['tags'].lower()
            q_lower = q['question'].lower()
            a_lower = q['answer'].lower()
            
            # Include if it mentions ML-related terms
            ml_terms = ['machine learning', 'neural', 'model', 'training', 'overfitting', 
                       'regularization', 'gradient', 'loss', 'bias-variance', 'cross-validation',
                       'ensemble', 'bagging', 'boosting', 'random forest', 'svm', 'regression',
                       'classification', 'supervised', 'unsupervised', 'deep learning']
            
            is_ml = any(term in q_lower or term in a_lower or term in tags_lower for term in ml_terms)
            
            if is_ml:
                ml_questions.append(q)
        
        print(f"✓ Filtered to {len(ml_questions)} Machine Learning questions")
        
        # Write to output file with proper formatting
        output_path = 'D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\scrapper_output.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("MACHINE LEARNING INTERVIEW QUESTIONS FOR ML ENGINEER\n")
            f.write("=" * 100 + "\n")
            f.write("Scraped from: https://cracked-ds-platform.vercel.app/\n")
            f.write("Role: ML Engineer (⚙️)\n")
            f.write("Category: Machine Learning (🤖) + Related Topics\n")
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
                    f.write(f"Tags: {qa['tags']}\n")
                if qa['companies']:
                    f.write(f"Companies: {qa['companies']}\n")
                
                f.write("\n")
        
        print(f"\n✓ SUCCESS!")
        print(f"  Machine Learning questions saved to: scrapper_output.txt")
        print(f"  Total questions: {len(ml_questions)}")
        
        return ml_questions
        
    except FileNotFoundError:
        print(f"✗ ERROR: Could not find {html_file}")
        print("  Please run the Selenium scraper first to generate the debug HTML file.")
        return []
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    questions = extract_ml_questions_from_html()
    print("\n" + "=" * 100)
    print("EXTRACTION COMPLETED!")
    print("=" * 100)
