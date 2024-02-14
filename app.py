import gradio as gr
import os
from dotenv import load_dotenv
from helper_functions import document_converter  # , initialize_pipeline

from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack import Pipeline

# Create document store
document_path = "documents"
documents = [f"{document_path}/{file}" for file in os.listdir(document_path)]
print(f"Number of documents: {len(documents)}")
document_store = document_converter(documents)

# Environment variables
load_dotenv(".env")

# Initialize Retriever
retriever = InMemoryBM25Retriever(document_store)

# Define a template prompt
prompt_template = """
You are a fashion guru who knows the future direction of the fashion 
industry. You know which trends are dying off and which are being 
introduced.  You can also identify potential future trends that may 
not have taken off yet.  You are also excellent at giving creative 
names to trends - something like 'gorpcore' or 'eclectic grandpa' -
generally really catchy names.  You are very confident in your responses
and never express doubt that the answer to a user's question
exists within the provided documents.

You should keep your responses somewhat concise, but but very clear about
what you are saying.  You should sound like you are saying novel or
insightful things, not just regurgitating well-known facts.

These are the documents you may reference for your expertise, 
but do not limit yourself to these.

{% for doc in documents %}
    {{ doc.content }}
{% endfor %}

\nQuestion: {{query}}
\nAnswer:
"""

prompt_builder = PromptBuilder(prompt_template)

# Initializing a generator
generator = OpenAIGenerator()


# Build the pipeline

p = Pipeline()
p.add_component("retriever", retriever)
p.add_component("prompt_builder", prompt_builder)
p.add_component("llm", generator)

p.connect("retriever", "prompt_builder.documents")
p.connect("prompt_builder", "llm")


def fashion_bot(message, history):
    result = p.run(
        {"retriever": {"query": message}, "prompt_builder": {"query": message}}
    )
    yield result["llm"]["replies"][0]


demo = gr.ChatInterface(
    fashion_bot,
    title="Future of Fashion Chatbot",
    description="""
        I am a Chatbot that can answer your questions about the current 
        and future state of the fashion industry.""",
    theme="glass",
    examples=[
        "What are some current micro-trends in sportswear?",
        "Which recent popular trends are now in decline?",
    ],
    cache_examples=True,
    retry_btn=None,
)

demo.launch()
