import re
import json

# Read the HTML file
with open('debug_page.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the ML topic definition and its questions array
# The pattern: {id:"ml",name:"Machine Learning",...questions:[...]}
# We need to extract from the ML topic start to where its questions array ends

# First, locate where ML topic starts
ml_start = content.find('{id:"ml",name:"Machine Learning"')
if ml_start == -1:
    print("ML topic not found!")
    exit(1)

print(f"ML topic starts at position {ml_start}")

# Find where the questions array starts within ML topic
questions_start = content.find('questions:[', ml_start)
if questions_start == -1:
    print("Questions array not found!")
    exit(1)

# Now we need to find where this questions array ends
# It ends with ]}, before the next topic {id:"..."
# We'll look for the pattern ]},\n{id:" which marks the end of one topic and start of next

# Start from questions_start and find the matching closing bracket
# We need to track bracket depth
pos = questions_start + len('questions:[')
bracket_depth = 1  # We're inside the questions array
brace_depth = 0

while pos < len(content) and bracket_depth > 0:
    if content[pos] == '[':
        bracket_depth += 1
    elif content[pos] == ']':
        bracket_depth -= 1
        if bracket_depth == 0:
            # Found the end of questions array
            break
    pos += 1

ml_end = pos + 1  # Include the closing ]

print(f"ML questions array ends at position {ml_end}")

# Extract the ML topic section
ml_section = content[ml_start:ml_end]

# Now parse the questions using regex
question_pattern = r"\{q:'([^']+(?:\\'[^']*)*)',a:'([^']+(?:\\'[^']*)*)'(?:,difficulty:'([^']*)')?(?:,tags:\[([^\]]*)\])?(?:,companies:\[([^\]]*)\])?\}"

matches = re.findall(question_pattern, ml_section, re.DOTALL)

print(f"\n✓ Found {len(matches)} Machine Learning category questions")

# Write to output file
output_file = 'scrapper_output.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("MACHINE LEARNING QUESTIONS (🤖 Category Only)\n")
    f.write(f"Total Questions: {len(matches)}\n")
    f.write("=" * 80 + "\n\n")
    
    for idx, (question, answer, difficulty, tags, companies) in enumerate(matches, 1):
        # Clean escaped quotes
        question = question.replace("\\'", "'")
        answer = answer.replace("\\'", "'")
        
        # Clean up tags and companies
        tags_list = [t.strip().strip("'\"") for t in tags.split(',')] if tags else []
        companies_list = [c.strip().strip("'\"") for c in companies.split(',')] if companies else []
        
        f.write(f"QUESTION {idx}\n")
        f.write("-" * 80 + "\n")
        f.write(f"Q: {question}\n\n")
        f.write(f"A: {answer}\n\n")
        
        if difficulty:
            f.write(f"Difficulty: {difficulty}\n")
        if tags_list:
            f.write(f"Tags: {', '.join(tags_list)}\n")
        if companies_list:
            f.write(f"Companies: {', '.join(companies_list)}\n")
        
        f.write("\n" + "=" * 80 + "\n\n")

print(f"\n✓ Successfully saved {len(matches)} questions to {output_file}")
print("\nFirst few questions:")
for i, (q, _, _, _, _) in enumerate(matches[:5], 1):
    print(f"{i}. {q.replace(chr(92)+"'", "'")[:80]}...")
