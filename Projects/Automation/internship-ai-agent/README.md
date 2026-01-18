# Internship AI Agent

Automated multi-agent system for discovering internship opportunities from Ahmedabad startups, focusing on AI/ML, Android, and Mobile App roles.

## Architecture

The system uses a modular agent-based architecture:

- **collector.py**: Scrapes startup listings and manages scan history
- **crawler.py**: Crawls startup websites to find career pages
- **classifier.py**: Classifies roles into categories (AI/ML, Android, Mobile, Web, Other)
- **scorer.py**: Scores opportunities based on location, role type, and internship availability
- **writer.py**: Writes results to Google Sheets

## Prerequisites

1. **Python 3.10**
2. **Google Cloud Service Account** with Sheets API enabled
3. **GitHub repository** for hosting and automation

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd D:\JAVA\CODE\Projects\Automation\internship-ai-agent
pip install -r requirements.txt
```

### 2. Create Google Sheets API Credentials

#### Step 2.1: Enable Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Sheets API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

#### Step 2.2: Create Service Account
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in service account details:
   - Name: `internship-agent`
   - Description: `Service account for internship discovery automation`
4. Click "Create and Continue"
5. Skip optional steps and click "Done"

#### Step 2.3: Generate JSON Key
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create new key"
4. Select "JSON" format
5. Download the JSON file (keep it secure)

#### Step 2.4: Create Google Sheet
1. Create a new Google Sheet named **"Internship Tracker"**
2. Share the sheet with the service account email:
   - Copy the service account email from JSON file (looks like `internship-agent@project-id.iam.gserviceaccount.com`)
   - Click "Share" in Google Sheets
   - Paste the service account email
   - Grant "Editor" permissions
3. Copy the **Spreadsheet ID** from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
   - Copy the `SPREADSHEET_ID` part

### 3. Local Testing

#### Step 3.1: Set Environment Variables

**Windows PowerShell:**
```powershell
$env:GOOGLE_CREDENTIALS_JSON = Get-Content "path\to\service-account-key.json" -Raw
$env:GOOGLE_SPREADSHEET_ID = "your_spreadsheet_id_here"
```

**Windows Command Prompt:**
```cmd
set GOOGLE_CREDENTIALS_JSON=<paste entire JSON content here>
set GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
```

**Linux/Mac:**
```bash
export GOOGLE_CREDENTIALS_JSON=$(cat path/to/service-account-key.json)
export GOOGLE_SPREADSHEET_ID="your_spreadsheet_id_here"
```

#### Step 3.2: Run the Agent
```bash
python main.py
```

### 4. GitHub Actions Setup

#### Step 4.1: Push Code to GitHub
```bash
cd D:\JAVA\CODE\Projects\Automation\internship-ai-agent
git init
git add .
git commit -m "Initial commit: Internship AI Agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/internship-ai-agent.git
git push -u origin main
```

#### Step 4.2: Add GitHub Secrets
1. Go to your GitHub repository
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Add two secrets:

**Secret 1: GOOGLE_CREDENTIALS_JSON**
- Name: `GOOGLE_CREDENTIALS_JSON`
- Value: Paste the entire content of your service account JSON file

**Secret 2: GOOGLE_SPREADSHEET_ID**
- Name: `GOOGLE_SPREADSHEET_ID`
- Value: Your Google Sheets spreadsheet ID

#### Step 4.3: Enable GitHub Actions
1. Go to "Actions" tab in your repository
2. If prompted, click "I understand my workflows, go ahead and enable them"

#### Step 4.4: Verify Workflow
The workflow will run:
- **Automatically**: Every day at 2:00 AM UTC (scheduled via cron)
- **Manually**: Go to "Actions" > "Internship AI Agent" > "Run workflow"

### 5. Customization

#### Change Schedule
Edit [.github/workflows/run.yml](.github/workflows/run.yml):
```yaml
schedule:
  - cron: '0 2 * * *'  # Change to your preferred time
```

Cron syntax:
- `0 2 * * *` = Daily at 2:00 AM UTC
- `0 */6 * * *` = Every 6 hours
- `0 9 * * 1` = Every Monday at 9:00 AM UTC

#### Change Target Cities
Edit [agents/collector.py](agents/collector.py):
```python
params = {
    'state': 'Gujarat',  # Change state
    'city': 'Ahmedabad',  # Change city
    'type': 'recognition'
}
```

#### Change Role Categories
Edit [agents/classifier.py](agents/classifier.py) to add/modify categories:
```python
self.categories = {
    'AI/ML': [...],
    'Android': [...],
    'Your Category': ['keyword1', 'keyword2']
}
```

#### Change Scoring Weights
Edit [agents/scorer.py](agents/scorer.py):
```python
self.weights = {
    'ahmedabad_location': 25,  # Adjust weights
    'startup': 20,
    'priority_role': 30,
    'internship_available': 20,
    'email_available': 5
}
```

## Output Format

The system writes to Google Sheets with these columns:

| Company | Role Category | Website | Email | Location | Score | Scan Date | Internship Available | Career Page URL |
|---------|---------------|---------|-------|----------|-------|-----------|----------------------|-----------------|

## Logging

The system provides detailed logging:
- Startup collection progress
- Crawling status for each company
- Classification results
- Scoring breakdown
- Google Sheets write status

## State Management

The [memory/state.json](memory/state.json) file tracks:
- Previously scanned companies with timestamps
- Last run timestamp
- Total opportunities found

Companies are re-scanned only after 30 days to avoid duplicates.

## Error Handling

The system handles:
- Network timeouts gracefully
- Missing career pages (falls back to homepage)
- Invalid URLs
- Google Sheets API errors
- State file corruption

## Troubleshooting

### "GOOGLE_CREDENTIALS_JSON not set"
Ensure environment variable is set correctly with complete JSON content.

### "Authentication failed"
Verify JSON key is valid and Google Sheets API is enabled.

### "No startups collected"
Check network connectivity and Startup India website availability. The system falls back to curated list.

### GitHub Actions fails
1. Verify secrets are set correctly in repository settings
2. Check Actions logs for specific error messages
3. Ensure repository has write permissions for state file updates

## Production Best Practices

1. **Secrets Management**: Never commit credentials to repository
2. **Rate Limiting**: System includes timeouts and retry logic
3. **Memory Management**: State file prevents duplicate scans
4. **Logging**: All operations logged for debugging
5. **Error Recovery**: Graceful failure handling with fallbacks

## License

MIT License - Feel free to modify and use for your needs.
