# Fashionbot

This is an LLM-based chatbot that answers questions about the current and future state of fashion.

## Steps to Deploy:

1. Create a free account on [Ploomber](https://ploomber.io/)

2. Create an Open AI Account to get an API Key

3. Add a .env text file to this directory (`/fashionbot/`) containing:
```
OPENAI_API_KEY='<Your Open AI API Key>'
```

4. Follow Ploomber CLI Instructions [here](https://docs.cloud.ploomber.io/en/latest/user-guide/cli.html)
    - `pip install ploomber-cloud`
    - `ploomber-cloud key <YOUR-PLOOMBER-API-KEY>`
        - Creates ploomber-cloud.json
        - Informs about creation of Github Workflow - I couldn't get this to work because I wasn't sure how to pass in the OPENAI_API_KEY (we don't want to store that on Github :-) ).
    - Initialize the app: `ploomber-cloud init`
    - Deploy the app: `ploomber-cloud deploy`


A few notes on deployment:

1.  There is a 50MB limit on the total file size.  We may not be able to pass all documents into the RAG for this example.
2.  You should remove your `.venv` if it exists in this directory.  Just make sure you create a `requirements.txt` file to rebuild from.
