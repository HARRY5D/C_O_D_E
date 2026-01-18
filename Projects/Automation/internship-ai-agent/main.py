import os
import sys
import json
import logging
from datetime import datetime
from typing import Dict, List

from agents.collector import StartupCollector
from agents.crawler import CareerPageCrawler
from agents.classifier import RoleClassifier
from agents.scorer import OpportunityScorer
from agents.writer import GoogleSheetsWriter


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class StateManager:
    def __init__(self, state_file: str = "memory/state.json"):
        self.state_file = state_file
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load state: {e}")
        
        return {
            "scanned_companies": {},
            "last_run": None,
            "total_opportunities_found": 0,
            "version": "1.0"
        }
    
    def save_state(self):
        try:
            os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            logger.info("State saved successfully")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    def get_last_scan(self, company_name: str) -> str:
        return self.state.get("scanned_companies", {}).get(company_name)
    
    def update_scan(self, company_name: str):
        if "scanned_companies" not in self.state:
            self.state["scanned_companies"] = {}
        self.state["scanned_companies"][company_name] = datetime.now().isoformat()
    
    def update_stats(self, opportunities_count: int):
        self.state["last_run"] = datetime.now().isoformat()
        self.state["total_opportunities_found"] = self.state.get("total_opportunities_found", 0) + opportunities_count


class InternshipAIAgent:
    def __init__(self):
        self.state_manager = StateManager()
        self.collector = StartupCollector(self.state_manager)
        self.crawler = CareerPageCrawler()
        self.classifier = RoleClassifier()
        self.scorer = OpportunityScorer()
        
        credentials_json = os.environ.get('GOOGLE_CREDENTIALS_JSON', '')
        spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID', '')
        
        if not credentials_json:
            logger.error("GOOGLE_CREDENTIALS_JSON environment variable not set")
            sys.exit(1)
        
        if not spreadsheet_id:
            logger.error("GOOGLE_SPREADSHEET_ID environment variable not set")
            sys.exit(1)
        
        self.writer = GoogleSheetsWriter(credentials_json, sheet_name="Sheet1")
        self.writer.set_spreadsheet_id(spreadsheet_id)
    
    def run(self):
        logger.info("=" * 80)
        logger.info("Starting Internship AI Agent")
        logger.info("=" * 80)
        
        try:
            startups = self.collector.collect_startups()
            
            if not startups:
                logger.warning("No startups collected. Exiting.")
                return
            
            logger.info(f"Processing {len(startups)} startups")
            
            opportunities = []
            
            for i, startup in enumerate(startups, 1):
                logger.info(f"\n[{i}/{len(startups)}] Processing: {startup['company_name']}")
                
                try:
                    crawled_data = self.crawler.crawl_startup(startup)
                    
                    classified_data = self.classifier.classify(crawled_data)
                    
                    scored_data = self.scorer.score(classified_data)
                    
                    if scored_data['score'] >= 30:
                        opportunities.append(scored_data)
                        logger.info(f"✓ Added opportunity: {scored_data['company_name']} (Score: {scored_data['score']})")
                    else:
                        logger.info(f"✗ Skipped {scored_data['company_name']} (Score too low: {scored_data['score']})")
                    
                    self.state_manager.update_scan(startup['company_name'])
                    
                except Exception as e:
                    logger.error(f"Error processing {startup['company_name']}: {e}")
                    continue
            
            if opportunities:
                opportunities.sort(key=lambda x: x['score'], reverse=True)
                
                logger.info(f"\n{'=' * 80}")
                logger.info(f"Found {len(opportunities)} high-quality opportunities")
                logger.info(f"{'=' * 80}")
                
                for opp in opportunities[:5]:
                    logger.info(f"  • {opp['company_name']} - {opp['role_category']} (Score: {opp['score']})")
                
                success = self.writer.write_opportunities(opportunities)
                
                if success:
                    logger.info("\n✓ Successfully wrote opportunities to Google Sheets")
                    self.state_manager.update_stats(len(opportunities))
                else:
                    logger.error("\n✗ Failed to write to Google Sheets")
            else:
                logger.info("\nNo opportunities met the scoring threshold")
            
            self.state_manager.save_state()
            
            logger.info("\n" + "=" * 80)
            logger.info("Internship AI Agent completed successfully")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Fatal error in main execution: {e}", exc_info=True)
            sys.exit(1)


def main():
    agent = InternshipAIAgent()
    agent.run()


if __name__ == "__main__":
    main()
