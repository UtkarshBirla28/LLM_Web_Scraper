import streamlit as st
from scraper.selenium_scraper import WebScraper
from config.config import MongoDB
from llm.openai_agent import LLMAgent
from utils.text_processor import clean_text
import time

def main():
    st.title("Web Scraper with LLM Integration")
    st.write("Enter a URL to scrape and ask questions about the content!")

    # Initialize components
    db = MongoDB()
    llm_agent = LLMAgent()

    # URL input
    url = st.text_input("Enter URL to scrape:")
    
    if st.button("Scrape"):
        with st.spinner("Scraping website..."):
            scraper = WebScraper()
            content = scraper.scrape_url(url)
            scraper.close()
            
            if content:
                # Clean and store the content
                cleaned_content = clean_text(content)
                data = {
                    "url": url,
                    "content": cleaned_content,
                    "timestamp": time.time()
                }
                db.insert_data(data)
                st.success("Content scraped and stored successfully!")
            else:
                st.error("Failed to scrape the website.")

    # Query section
    st.subheader("Ask Questions")
    query = st.text_input("Enter your question:")
    
    if st.button("Get Answer"):
        with st.spinner("Processing your question..."):
            # Get all scraped data
            scraped_data = db.get_all_data()
            
            if not scraped_data:
                st.warning("No scraped data available. Please scrape a website first.")
                return
            
            # Combine all content for context
            context = " ".join([data["content"] for data in scraped_data])
            
            # Get response from LLM
            response = llm_agent.process_query(query, context)
            
            if response:
                st.write("Answer:", response)
            else:
                st.error("Failed to process your question.")

if __name__ == "__main__":
    main()