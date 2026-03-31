from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

def scrape_ml_questions():
    """
    Scrape Machine Learning questions for ML Engineer from cracked-ds-platform
    """
    url = "https://cracked-ds-platform.vercel.app/"
    
    print("Starting ML Questions Scraper for ML Engineer role...")
    print("=" * 100)
    
    # Setup Edge options
    edge_options = Options()
    # edge_options.add_argument('--headless')  # Uncomment to run in background
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--window-size=1920,1080')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    questions = []
    
    try:
        print("\n[1/6] Initializing browser...")
        # Use Edge driver from system PATH (no download needed)
        driver = webdriver.Edge(options=edge_options)
        
        print(f"[2/6] Loading website: {url}")
        driver.get(url)
        time.sleep(5)
        
        # Wait for page to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        print("[3/6] Navigating to ML Engineer section...")
        
        # Find and click ML Engineer (⚙️ ML Engineer - 420 questions)
        ml_engineer_clicked = False
        attempts = 0
        max_attempts = 3
        
        while not ml_engineer_clicked and attempts < max_attempts:
            try:
                # Look for the ML Engineer button/link
                all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'ML Engineer') or contains(text(), '⚙️')]")
                
                for elem in all_elements:
                    text = elem.text
                    if 'ML Engineer' in text or ('420' in text and 'ML' in driver.page_source):
                        print(f"  ✓ Found ML Engineer section: {text[:50]}")
                        driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", elem)
                        ml_engineer_clicked = True
                        time.sleep(4)
                        break
                
                if not ml_engineer_clicked:
                    attempts += 1
                    time.sleep(2)
            except Exception as e:
                attempts += 1
                time.sleep(2)
        
        if not ml_engineer_clicked:
            print("  ⚠ Could not find ML Engineer section, continuing with current page...")
        
        print("[4/6] Navigating to Machine Learning questions...")
        
        # Find and click Machine Learning category (🤖 Machine Learning - 3/63 completed)
        ml_category_clicked = False
        attempts = 0
        
        while not ml_category_clicked and attempts < max_attempts:
            try:
                # Look for Machine Learning category
                all_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Machine Learning') or contains(text(), '🤖')]")
                
                for elem in all_elements:
                    text = elem.text
                    if 'Machine Learning' in text and ('63' in text or 'completed' in text):
                        print(f"  ✓ Found Machine Learning category: {text[:50]}")
                        driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                        time.sleep(1)
                        driver.execute_script("arguments[0].click();", elem)
                        ml_category_clicked = True
                        time.sleep(4)
                        break
                
                if not ml_category_clicked:
                    attempts += 1
                    time.sleep(2)
            except Exception as e:
                attempts += 1
                time.sleep(2)
        
        if not ml_category_clicked:
            print("  ⚠ Could not find Machine Learning category, continuing with current page...")
        
        print("[5/6] Extracting questions and answers...")
        
        # Scroll to load all content
        print("  Scrolling to load all questions...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        
        while scroll_attempts < 5:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
        
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Save page for debugging
        with open('D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\debug_page.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Extract all text to analyze
        full_text = soup.get_text(separator='\n')
        
        # Try to find question cards or containers
        print("  Analyzing page structure...")
        
        # Method 1: Find expandable/collapsible question elements
        all_buttons = driver.find_elements(By.TAG_NAME, "button")
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        
        question_elements = []
        
        # Try clicking on question elements to expand them
        for btn in all_buttons[:100]:  # Limit to first 100 buttons
            try:
                text = btn.text.strip()
                # If button text looks like a question or has question-like patterns
                if text and (
                    '?' in text or 
                    text.lower().startswith(('what', 'how', 'why', 'explain', 'describe', 'define')) or
                    len(text) > 30
                ):
                    question_elements.append(btn)
            except:
                pass
        
        print(f"  Found {len(question_elements)} potential question elements")
        
        # Try expanding and extracting questions
        extracted_count = 0
        for i, elem in enumerate(question_elements[:63]):  # Limit to 63 (total ML questions)
            try:
                # Get question text before clicking
                q_text = elem.text.strip()
                
                if len(q_text) < 10 or len(q_text) > 500:
                    continue
                
                # Scroll into view and click to expand
                driver.execute_script("arguments[0].scrollIntoView(true);", elem)
                time.sleep(0.5)
                
                try:
                    driver.execute_script("arguments[0].click();", elem)
                    time.sleep(1)
                except:
                    pass
                
                # Try to find expanded content/answer
                parent = elem
                for _ in range(3):
                    parent = driver.execute_script("return arguments[0].parentElement;", parent)
                    if parent is None:
                        break
                
                answer_text = ""
                if parent:
                    try:
                        answer_text = parent.text.replace(q_text, '').strip()
                    except:
                        pass
                
                # Add to questions list
                if not any(q['question'] == q_text for q in questions):
                    questions.append({
                        'question': q_text,
                        'answer': answer_text[:2000] if answer_text else ""
                    })
                    extracted_count += 1
                    
                    if extracted_count % 10 == 0:
                        print(f"  Extracted {extracted_count} questions...")
                
            except Exception as e:
                continue
        
        # Method 2: Parse HTML for question patterns
        print("  Parsing HTML for additional questions...")
        
        all_text_elements = soup.find_all(['div', 'p', 'span', 'li', 'h3', 'h4'])
        
        for elem in all_text_elements:
            text = elem.get_text(strip=True)
            
            # Check if this looks like a question
            if text and 10 < len(text) < 500:
                is_question = (
                    '?' in text or
                    text.lower().startswith(('what ', 'how ', 'why ', 'when ', 'explain ', 'define ', 'describe ', 'compare '))
                )
                
                if is_question:
                    # Try to find answer in next sibling or parent
                    answer = ""
                    next_elem = elem.find_next_sibling()
                    if next_elem:
                        answer = next_elem.get_text(strip=True)
                    
                    # Check for duplicates
                    if not any(q['question'] == text for q in questions):
                        questions.append({
                            'question': text,
                            'answer': answer[:2000] if answer else ""
                        })
        
        print(f"  ✓ Total questions extracted: {len(questions)}")
        
        print("[6/6] Saving questions to file...")
        
        # Write to output file
        output_path = 'D:\\JAVA\\CODE\\PYTHON\\PRACTICAL\\EXTRA_FILES\\scrapper_output.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write("MACHINE LEARNING INTERVIEW QUESTIONS FOR ML ENGINEER\n")
            f.write("=" * 100 + "\n")
            f.write("Scraped from: https://cracked-ds-platform.vercel.app/\n")
            f.write("Role: ML Engineer (⚙️)\n")
            f.write("Category: Machine Learning (🤖)\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Questions: {len(questions)}\n")
            f.write("=" * 100 + "\n\n")
            
            if len(questions) == 0:
                f.write("⚠ NOTE: No questions were automatically extracted.\n\n")
                f.write("This website uses dynamic content that may require:\n")
                f.write("1. Manual interaction to reveal questions\n")
                f.write("2. API access or authentication\n")
                f.write("3. Different scraping approach\n\n")
                f.write("Please check debug_page.html for the actual page content.\n")
            else:
                for idx, qa in enumerate(questions, 1):
                    f.write(f"\n{'=' * 100}\n")
                    f.write(f"QUESTION {idx}\n")
                    f.write(f"{'=' * 100}\n\n")
                    f.write(f"{qa['question']}\n\n")
                    
                    if qa['answer'] and len(qa['answer']) > 10:
                        f.write(f"{'-' * 100}\n")
                        f.write(f"ANSWER:\n")
                        f.write(f"{'-' * 100}\n\n")
                        f.write(f"{qa['answer']}\n\n")
                    else:
                        f.write(f"{'-' * 100}\n")
                        f.write(f"ANSWER: [Manual extraction needed]\n")
                        f.write(f"{'-' * 100}\n\n")
        
        print(f"\n✓ SUCCESS!")
        print(f"  Output saved to: scrapper_output.txt")
        print(f"  Debug HTML saved to: debug_page.html")
        print(f"  Total questions extracted: {len(questions)}")
        
        return questions
        
    except Exception as e:
        print(f"\n✗ ERROR during scraping: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()

if __name__ == "__main__":
    questions = scrape_ml_questions()
    print("\n" + "=" * 100)
    print("SCRAPING COMPLETED!")
    print("=" * 100)
