from Selenuim_Scraper.scraper import WebScraper
from Process import chunking_data ,find_most_relevant_chunks
import gradio as gr
import ollama


def process_query(user_input):
    scraper = WebScraper()

    scraper.user_search(user_input)

    data = scraper.scrape_data()

    chunks = chunking_data(data)
    most_relevant = find_most_relevant_chunks(user_input ,chunks)

    return " \n ".join(most_relevant)



def predict(user_input ,progress=gr.Progress()):

    progress(0.1, desc="Searching the web...")

    final_text = process_query(user_input)

    progress(0.6, desc="Summarizing data with Ollama...")

    system_prompt = (
        "You are a 'Search-to-Summary' AI Assistant. Your task is to synthesize the "
        "provided web-scraped context into a cohesive response for the user."
        "\n\n"
        "Guidelines:\n"
        "1. **Accuracy First**: Only use the provided context. If the context doesn't "
        "contain the answer, say 'I couldn't find specific information on that.'\n"
        "2. **Structure**: Use Markdown headings (##) and bullet points for clarity.\n"
        "3. **Synthesis**: Do not just list the chunks. Merge overlapping information "
        "from different websites into a single narrative.\n"
        "4. **Citations**: If a chunk includes a source name or URL, mention it.\n"
        "5. **No Noise**: Ignore navigation text like 'Click here' or 'Sign up' that "
        "might have slipped through the scraper."
    )

    user_message = f"USER QUERY: {user_input}\n\nWEB CONTEXT:\n{final_text}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:

        stream = ollama.chat(model="llama3.2:latest", messages=messages ,stream=True)
        full_response = ""
        for chunk in stream:
            # Extract the new text part
            content = chunk['message']['content']
            full_response += content
            # 'yield' updates the Gradio UI after every word/character
            yield full_response
        progress(1.0, desc="Done!")

    except Exception as e:
        return f"Error: {str(e)}"

with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("# AI Web Searcher")
    gr.Markdown("Enter a question. I will search the live web, scrape data, and find the best answer.")

    with gr.Row():
        user_input = gr.Textbox(
            label="Your Question",
            placeholder="e.g. What is Python ?",
            scale=4
        )
        submit_btn = gr.Button("Search", variant="primary", scale=1)

    output_display = gr.Markdown(label="Search Result")

    submit_btn.click(
        fn=predict,
        inputs=user_input,
        outputs=output_display
    )

demo.launch()