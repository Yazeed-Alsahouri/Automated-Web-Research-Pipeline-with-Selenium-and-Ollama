# Automated-Web-Research-Pipeline-with-Selenium-and-Ollama
This project presents a sophisticated, end-to-end Retrieval-Augmented Generation (RAG) pipeline designed to bridge the gap between real-time web discovery and local AI-driven synthesis. The system automates the entire research workflow: from identifying relevant web sources via automated search and extracting dynamic content using Selenium, to processing that data into semantic knowledge chunks and generating cohesive, streaming summaries through a locally hosted Large Language Model (LLM).

Unlike static knowledge bases, this pipeline operates on live web data, demonstrating how modern automation tools and RAG architectures can be combined to create a private, high-performance "Deep Research" assistant that requires no external API subscriptions.

# Workflow Overview
![Alt text for the image](images/Flow.png)

# System Architecture & Pipeline Components
The project is structured into modular components that form a unified data ingestion, processing, and AI-powered synthesis pipeline:

   1. Dynamic Web Data Ingestion (Selenium-Based Scraping):

      - Automated Search: Programmatically interfaces with search engines to identify the most relevant URLs based on the user's natural language query.

      - Dynamic Extraction: Utilizes Selenium WebDriver in headless mode to navigate complex, JavaScript-heavy websites that traditional scrapers cannot access.

      - Content Cleaning: Extracts raw textual data from web elements, filtering out boilerplate content such as navigation bars, footers, and advertisements to ensure high-quality context for the LLM.

   2. Semantic Data Processing (RAG Workflow):
      
      - Recursive Character Splitting: Implements intelligent text chunking that respects document structure (paragraphs and sentences) while maintaining overlap to preserve semantic context across fragments.

      - Similarity Search: Utilizes Sentence-Transformers to embed the scraped text into a vector space, allowing the system to perform a mathematical similarity search to find the "needle in the haystack"—the specific chunks most relevant to the user's question.

      - Context Injection: Filters out noise and ranks the top-N most relevant fragments to be used as the "ground truth" for the generation phase.

   3. Knowledge Synthesis Using Local LLM (Ollama):
      
      - Local Inference: Integrates Llama 3.2 (via Ollama) for fully private, local inference, ensuring that research data never leaves the user's machine.

      - System Prompt Engineering: Employs a specialized "Search-to-Summary" system prompt that forces the model to synthesize information across multiple sources, prioritize accuracy, and use Markdown for structured reporting.

   4. Interactive Interface (Gradio):
    
      - Asynchronous UI: Built with Gradio Blocks, featuring a layout optimized for research: user input on the left and a expansive Markdown research report on the right.

![Alt text for the image](images/Gradio.png)











