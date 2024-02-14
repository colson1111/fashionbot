import pandas as pd
import os
from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.document_stores.in_memory import InMemoryDocumentStore

from haystack.components.writers import DocumentWriter

from haystack.components.builders import PromptBuilder
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import AnswerBuilder
from haystack.components.builders import PromptBuilder

# from haystack.utils import convert_files_to_docs
# from haystack.nodes import PreProcessor


def document_converter(directory: str):
    """
    Prepares files in given directory
    """
    document_store = InMemoryDocumentStore()
    pipeline = Pipeline()
    pipeline.add_component("converter", PyPDFToDocument())
    pipeline.add_component("cleaner", DocumentCleaner())
    pipeline.add_component(
        "splitter",
        DocumentSplitter(split_by="word", split_length=100),
    )
    pipeline.add_component("writer", DocumentWriter(document_store=document_store))
    pipeline.connect("converter", "cleaner")
    pipeline.connect("cleaner", "splitter")
    pipeline.connect("splitter", "writer")
    pipeline.run({"converter": {"sources": directory}})

    return document_store


def initialize_pipeline(document_store, openai_key):
    """
    Initialize the pipeline for the AI chatbot

    Args:
        document_store (DocumentStore): Haystack document store containing docs
        openai_key (str): OpenAI Key

    Returns:
        prediction_pipeline (Pipeline): Prediction pipeline
    """

    try:
        prompt_template = """
        You are a fashion guru who knows the future direction of the fashion 
        industry. You know which trends are dying off and which are being 
        introduced.  You can also identify potential future trends that may 
        not have taken off yet.  You are also excellent at giving creative 
        names to trends - something like 'gorpcore' or 'eclectic grandpa' -
        generally really catchy names.

        These are the documents you may reference for your expertise, 
        but do not limit yourself to these.

        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}

        \nQuestion: {{query}}
        \nAnswer:
        """

        retriever = InMemoryBM25Retriever(document_store)
        prompt_builder = PromptBuilder(prompt_template)
        generator = OpenAIGenerator()

        p = Pipeline()
        p.add_component("retriever", retriever)
        p.add_component("prompt_builder", prompt_builder)
        p.add_component("llm", generator)

        p.connect("retriever", "prompt_builder.documents")
        p.connect("prompt_builder", "llm")
        return p

    except Exception as e:
        print("Unable to initialize pipeline due to: ", e)
        return None
