"""
Streamlit UI for Newsletter Generator
"""
import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from db.database import Database
from pipeline.fact_sheet_builder import FactSheetBuilder
from pipeline.scheduler import NewsletterScheduler
from llm.style_extractor import StyleExtractor
from llm.newsletter_generator import NewsletterGenerator
from config.settings import FREQUENCY_OPTIONS

# Page configuration
st.set_page_config(
    page_title="Newsletter Generator",
    page_icon="📰",
    layout="wide"
)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()

if 'scheduler' not in st.session_state:
    st.session_state.scheduler = NewsletterScheduler(st.session_state.db)

# Sidebar navigation
st.sidebar.title("📰 Newsletter Generator")
page = st.sidebar.radio(
    "Navigation",
    ["Topics Manager", "Writing Samples", "Fact Sheets", "Generate Newsletter"]
)

# Topics Manager Page
if page == "Topics Manager":
    st.title("Topics Manager")
    
    # Add new topic
    with st.expander("➕ Add New Topic", expanded=False):
        with st.form("add_topic_form"):
            topic_name = st.text_input("Topic Name", placeholder="e.g., Artificial Intelligence")
            frequency = st.selectbox(
                "Frequency",
                options=list(FREQUENCY_OPTIONS.keys()),
                index=1  # Default to weekly
            )
            submit = st.form_submit_button("Add Topic")
            
            if submit:
                if topic_name:
                    try:
                        topic_id = st.session_state.db.add_topic(topic_name, frequency)
                        st.success(f"Topic '{topic_name}' added successfully!")
                        st.rerun()
                    except ValueError as e:
                        st.error(str(e))
                else:
                    st.error("Please enter a topic name")
    
    # Display all topics
    st.subheader("All Topics")
    topics = st.session_state.db.get_all_topics()
    
    if topics:
        for topic in topics:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{topic['topic_name']}**")
                
                with col2:
                    st.write(f"Frequency: {topic['frequency']}")
                
                with col3:
                    if topic['last_run']:
                        try:
                            last_run = datetime.fromisoformat(topic['last_run'])
                            st.write(f"Last run: {last_run.strftime('%Y-%m-%d %H:%M')}")
                        except:
                            st.write("Last run: Never")
                    else:
                        st.write("Last run: Never")
                
                with col4:
                    if st.button("Run Now", key=f"run_{topic['id']}"):
                        with st.spinner("Running pipeline..."):
                            try:
                                st.session_state.scheduler.run_manual(topic['id'])
                                st.success("Pipeline completed!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                
                st.divider()
    else:
        st.info("No topics yet. Add your first topic above!")

# Writing Samples Page
elif page == "Writing Samples":
    st.title("Writing Samples")
    st.write("Upload writing samples to train the newsletter generator on your writing style.")
    
    # Get topics for selection
    topics = st.session_state.db.get_all_topics()
    
    if topics:
        selected_topic_id = st.selectbox(
            "Select Topic",
            options=[t['id'] for t in topics],
            format_func=lambda x: next(t['topic_name'] for t in topics if t['id'] == x)
        )
        
        # Upload writing sample
        st.subheader("Upload Writing Sample")
        uploaded_file = st.file_uploader(
            "Upload a text file or paste text",
            type=['txt', 'md'],
            help="Upload a file containing your writing samples"
        )
        
        sample_text = st.text_area(
            "Or paste text directly",
            height=200,
            placeholder="Paste your writing sample here..."
        )
        
        if st.button("Save Writing Sample"):
            text_to_save = ""
            
            if uploaded_file:
                text_to_save = uploaded_file.read().decode('utf-8')
            elif sample_text:
                text_to_save = sample_text
            
            if text_to_save:
                try:
                    st.session_state.db.add_writing_sample(selected_topic_id, text_to_save)
                    st.success("Writing sample saved!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide a writing sample")
        
        # Display existing samples
        st.subheader("Existing Writing Samples")
        samples = st.session_state.db.get_writing_samples(selected_topic_id)
        
        if samples:
            for idx, sample in enumerate(samples, 1):
                with st.expander(f"Sample {idx} - {sample['created_at']}"):
                    st.text_area(
                        "Content",
                        value=sample['text'],
                        height=150,
                        key=f"sample_{sample['id']}",
                        disabled=True
                    )
        else:
            st.info("No writing samples for this topic yet.")
    else:
        st.warning("Please add a topic first in the Topics Manager page.")

# Fact Sheets Page
elif page == "Fact Sheets":
    st.title("Fact Sheets")
    st.write("View generated fact sheets before newsletter generation.")
    
    topics = st.session_state.db.get_all_topics()
    
    if topics:
        selected_topic_id = st.selectbox(
            "Select Topic",
            options=[t['id'] for t in topics],
            format_func=lambda x: next(t['topic_name'] for t in topics if t['id'] == x)
        )
        
        # Manual fact sheet generation
        st.info("ℹ️ **Note**: Research papers (arXiv, Semantic Scholar) work immediately. News, LinkedIn, and web scraping require Playwright MCP integration. See MCP_INTEGRATION.md for setup.")
        
        if st.button("Generate New Fact Sheet"):
            topic_name = next(t['topic_name'] for t in topics if t['id'] == selected_topic_id)
            with st.spinner("Generating fact sheet..."):
                try:
                    builder = FactSheetBuilder()
                    # Try to use MCP if available, otherwise just use research papers
                    fact_sheet = builder.build_fact_sheet(topic_name, use_mcp_client=None)
                    st.session_state.db.save_fact_sheet(
                        selected_topic_id,
                        fact_sheet['markdown'],
                        fact_sheet['json_data']
                    )
                    st.success("Fact sheet generated!")
                    
                    # Show summary
                    json_data = fact_sheet['json_data']
                    st.write(f"**Summary:**")
                    st.write(f"- Research Papers: {len(json_data.get('research_papers', []))}")
                    st.write(f"- News Headlines: {len(json_data.get('news_headlines', []))}")
                    st.write(f"- LinkedIn Posts: {len(json_data.get('linkedin_posts', []))}")
                    st.write(f"- Web Articles: {len(json_data.get('web_articles', []))}")
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(traceback.format_exc())
        
        # Display fact sheets
        fact_sheets = st.session_state.db.get_all_fact_sheets(selected_topic_id)
        
        if fact_sheets:
            st.subheader("Fact Sheet History")
            for idx, sheet in enumerate(fact_sheets, 1):
                with st.expander(f"Fact Sheet {idx} - {sheet['created_at']}"):
                    st.markdown(sheet['markdown'])
                    
                    # Show JSON data
                    if st.checkbox(f"Show JSON Data", key=f"json_{sheet['id']}"):
                        json_data = json.loads(sheet['json_data'])
                        st.json(json_data)
        else:
            st.info("No fact sheets for this topic yet. Generate one above!")
    else:
        st.warning("Please add a topic first in the Topics Manager page.")

# Generate Newsletter Page
elif page == "Generate Newsletter":
    st.title("Generate Newsletter")
    st.write("Generate newsletters from fact sheets using your writing style.")
    
    topics = st.session_state.db.get_all_topics()
    
    if topics:
        selected_topic_id = st.selectbox(
            "Select Topic",
            options=[t['id'] for t in topics],
            format_func=lambda x: next(t['topic_name'] for t in topics if t['id'] == x)
        )
        
        topic_name = next(t['topic_name'] for t in topics if t['id'] == selected_topic_id)
        
        # Check for fact sheet
        fact_sheet = st.session_state.db.get_latest_fact_sheet(selected_topic_id)
        
        if not fact_sheet:
            st.warning("No fact sheet found. Please generate one in the Fact Sheets page first.")
        else:
            # Get writing samples
            writing_samples = st.session_state.db.get_writing_samples(selected_topic_id)
            
            if st.button("Generate Newsletter"):
                with st.spinner("Generating newsletter..."):
                    try:
                        # Extract style
                        if writing_samples:
                            sample_texts = [s['text'] for s in writing_samples]
                            style_extractor = StyleExtractor()
                            style_profile = style_extractor.extract_style(sample_texts)
                        else:
                            style_profile = {"tone": "professional", "structure": "clear paragraphs", "voice": "third person", "common_phrases": []}
                            st.info("No writing samples found. Using default style.")
                        
                        # Generate newsletter
                        generator = NewsletterGenerator()
                        newsletter = generator.generate(
                            fact_sheet['markdown'],
                            style_profile,
                            topic_name
                        )
                        
                        # Save newsletter
                        st.session_state.db.save_newsletter(selected_topic_id, newsletter)
                        st.success("Newsletter generated!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            # Display latest newsletter
            newsletter = st.session_state.db.get_latest_newsletter(selected_topic_id)
            
            if newsletter:
                st.subheader("Latest Newsletter")
                st.markdown(newsletter['markdown'])
                
                # Export options
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "Download as Markdown",
                        data=newsletter['markdown'],
                        file_name=f"newsletter_{topic_name}_{newsletter['created_at']}.md",
                        mime="text/markdown"
                    )
            else:
                st.info("No newsletter generated yet. Click 'Generate Newsletter' above!")
    else:
        st.warning("Please add a topic first in the Topics Manager page.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Status:**")
if st.session_state.scheduler.running:
    st.sidebar.success("Scheduler: Running")
else:
    st.sidebar.info("Scheduler: Stopped")

if st.sidebar.button("Start Scheduler"):
    st.session_state.scheduler.start()
    st.sidebar.success("Scheduler started!")
    st.rerun()

if st.sidebar.button("Stop Scheduler"):
    st.session_state.scheduler.stop()
    st.sidebar.info("Scheduler stopped!")
    st.rerun()

