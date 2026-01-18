import os
import json
import logging
from datetime import datetime
from typing import List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


class GoogleSheetsWriter:
    def __init__(self, credentials_json: str, sheet_name: str = "Internship Tracker"):
        self.sheet_name = sheet_name
        self.service = self._authenticate(credentials_json)
        self.spreadsheet_id = None
    
    def _authenticate(self, credentials_json: str):
        try:
            credentials_dict = json.loads(credentials_json)
            credentials = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets authentication successful")
            return service
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise
    
    def set_spreadsheet_id(self, spreadsheet_id: str):
        self.spreadsheet_id = spreadsheet_id
        logger.info(f"Using spreadsheet ID: {spreadsheet_id}")
    
    def write_opportunities(self, opportunities: List[Dict]) -> bool:
        if not self.spreadsheet_id:
            logger.error("Spreadsheet ID not set")
            return False
        
        if not opportunities:
            logger.warning("No opportunities to write")
            return True
        
        try:
            self._ensure_headers()
            
            rows = []
            for opp in opportunities:
                row = [
                    opp.get('company_name', ''),
                    opp.get('role_category', ''),
                    opp.get('website', ''),
                    opp.get('email', ''),
                    opp.get('location', ''),
                    opp.get('score', 0),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'Yes' if opp.get('is_internship', False) else 'No',
                    opp.get('career_page_url', '')
                ]
                rows.append(row)
            
            body = {
                'values': rows
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A2",
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            logger.info(f"Successfully wrote {len(rows)} opportunities to Google Sheets")
            return True
            
        except HttpError as e:
            logger.error(f"Google Sheets API error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error writing to sheets: {e}")
            return False
    
    def _ensure_headers(self):
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{self.sheet_name}!A1:I1"
            ).execute()
            
            values = result.get('values', [])
            
            if not values or len(values[0]) < 9:
                headers = [
                    'Company',
                    'Role Category',
                    'Website',
                    'Email',
                    'Location',
                    'Score',
                    'Scan Date',
                    'Internship Available',
                    'Career Page URL'
                ]
                
                body = {
                    'values': [headers]
                }
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{self.sheet_name}!A1:I1",
                    valueInputOption='USER_ENTERED',
                    body=body
                ).execute()
                
                logger.info("Created headers in Google Sheet")
        
        except Exception as e:
            logger.error(f"Error ensuring headers: {e}")
