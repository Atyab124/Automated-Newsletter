"""
Scheduler for automated newsletter generation
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
from typing import Optional, Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from db.database import Database
from pipeline.fact_sheet_builder import FactSheetBuilder
from llm.style_extractor import StyleExtractor
from llm.newsletter_generator import NewsletterGenerator
from config.settings import FREQUENCY_OPTIONS, LLM_PROVIDER


class NewsletterScheduler:
    """Manages scheduled newsletter generation"""
    
    def __init__(self, db: Database, mcp_client=None):
        self.db = db
        self.scheduler = BackgroundScheduler()
        self.fact_sheet_builder = FactSheetBuilder()
        self.style_extractor = StyleExtractor(provider=LLM_PROVIDER)
        self.newsletter_generator = NewsletterGenerator(provider=LLM_PROVIDER)
        self.mcp_client = mcp_client
        self.running = False
    
    def start(self):
        """Start the scheduler"""
        if not self.running:
            # Run check every hour
            self.scheduler.add_job(
                self._check_and_run_pipeline,
                trigger=IntervalTrigger(hours=1),
                id='newsletter_check',
                replace_existing=True
            )
            self.scheduler.start()
            self.running = True
    
    def stop(self):
        """Stop the scheduler"""
        if self.running:
            self.scheduler.shutdown()
            self.running = False
    
    def _check_and_run_pipeline(self):
        """Check all topics and run pipeline if due"""
        topics = self.db.get_all_topics()
        
        for topic in topics:
            if self._should_run(topic):
                try:
                    self._run_pipeline(topic['id'], topic['topic_name'])
                except Exception as e:
                    print(f"Error running pipeline for topic {topic['topic_name']}: {e}")
    
    def _should_run(self, topic: Dict) -> bool:
        """Check if pipeline should run for a topic"""
        frequency = topic.get('frequency', 'weekly')
        last_run = topic.get('last_run')
        
        if not last_run:
            return True  # Never run before
        
        # Parse last_run
        try:
            if isinstance(last_run, str):
                last_run_dt = datetime.fromisoformat(last_run)
            else:
                last_run_dt = last_run
        except:
            return True  # If parsing fails, run it
        
        # Get frequency in days
        frequency_days = FREQUENCY_OPTIONS.get(frequency, 7)
        
        # Check if enough time has passed
        next_run = last_run_dt + timedelta(days=frequency_days)
        return datetime.now() >= next_run
    
    def _run_pipeline(self, topic_id: int, topic_name: str):
        """Run the full pipeline for a topic"""
        print(f"Running pipeline for topic: {topic_name}")
        
        # Step 1: Build fact sheet
        fact_sheet = self.fact_sheet_builder.build_fact_sheet(
            topic_name,
            use_mcp_client=self.mcp_client
        )
        
        # Step 2: Save fact sheet
        self.db.save_fact_sheet(
            topic_id,
            fact_sheet['markdown'],
            fact_sheet['json_data']
        )
        
        # Step 3: Get writing samples and extract style
        writing_samples = self.db.get_writing_samples(topic_id)
        sample_texts = [sample['text'] for sample in writing_samples]
        style_profile = self.style_extractor.extract_style(sample_texts)
        
        # Step 4: Generate newsletter
        newsletter = self.newsletter_generator.generate(
            fact_sheet['markdown'],
            style_profile,
            topic_name
        )
        
        # Step 5: Save newsletter
        self.db.save_newsletter(topic_id, newsletter)
        
        # Step 6: Update last_run
        self.db.update_topic_last_run(topic_id, datetime.now())
        
        print(f"Pipeline completed for topic: {topic_name}")
    
    def run_manual(self, topic_id: int):
        """Manually trigger pipeline for a topic"""
        topic = self.db.get_topic(topic_id)
        if topic:
            self._run_pipeline(topic_id, topic['topic_name'])

