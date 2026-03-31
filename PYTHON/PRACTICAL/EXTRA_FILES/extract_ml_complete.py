import re

# Read the HTML file
with open('debug_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the ML topic start
ml_start = content.find('{id:"ml",name:"Machine Learning"')
if ml_start == -1:
    print("ML topic not found!")
    exit(1)

print(f"ML topic starts at position {ml_start}")

# Find the next topic after ML (it will start with },\n{id or ]},\n{id)
# We need to find where ML topic ends by finding the next topic
next_topic = content.find('},\n{id:', ml_start + 100)
if next_topic == -1:
    # Try alternative pattern
    next_topic = content.find(']},\n{id:', ml_start + 100)

if next_topic == -1:
    print("Could not find next topic boundary!")
    exit(1)

# The ML section ends at the closing brace before the next topic
ml_end = next_topic + 1  # Include the closing }

print(f"ML section ends at position {ml_end} (before next topic)")

# Extract the ML topic section
ml_section = content[ml_start:ml_end]

print(f"Extracted section length: {len(ml_section)} characters")

# Now parse all questions within this section using regex
question_pattern = r"\{q:'([^']+(?:\\'[^']*)*)',a:'([^']+(?:\\'[^']*)*)'(?:,difficulty:'([^']*)')?(?:,tags:\[([^\]]*)\])?(?:,companies:\[([^\]]*)\])?\}"

matches = re.findall(question_pattern, ml_section, re.DOTALL)

print(f"\n✓ Found {len(matches)} Machine Learning questions")

# Write to output file
output_file = 'scrapper_output.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("MACHINE LEARNING QUESTIONS (🤖 Category)\n")
    f.write(f"Scraped from: https://cracked-ds-platform.vercel.app/\n")
    f.write(f"Total Questions: {len(matches)}\n")
    f.write("=" * 80 + "\n\n")
    
    for idx, (question, answer, difficulty, tags, companies) in enumerate(matches, 1):
        # Clean escaped quotes
        question = question.replace("\\'", "'")
        answer = answer.replace("\\'", "'")
        # Also clean \n literals to actual newlines for better readability
        answer = answer.replace("\\n", "\n")
        
        # Clean up tags and companies
        tags_list = [t.strip().strip("'\"") for t in tags.split(',')] if tags else []
        companies_list = [c.strip().strip("'\"") for c in companies.split(',')] if companies else []
        
        f.write(f"QUESTION {idx}\n")
        f.write("-" * 80 + "\n")
        f.write(f"Q: {question}\n\n")
        f.write(f"ANSWER:\n{answer}\n\n")
        
        if difficulty:
            f.write(f"Difficulty: {difficulty}\n")
        if tags_list:
            f.write(f"Tags: {', '.join(tags_list)}\n")
        if companies_list:
            f.write(f"Companies: {', '.join(companies_list)}\n")
        
        f.write("\n" + "=" * 80 + "\n\n")

print(f"\n✓ Successfully saved {len(matches)} questions to {output_file}")
print("\nFirst 5 questions:")
for i, (q, _, _, _, _) in enumerate(matches[:5], 1):
    print(f"  {i}. {q.replace(chr(92)+'  ', '   ')[:70]}...")

print("\nLast 5 questions:")
for i, (q, _, _, _, _) in enumerate(matches[-5:], len(matches)-4):
    print(f"  {i}. {q.replace(chr(92)+'  ', '   ')[:70]}...")
