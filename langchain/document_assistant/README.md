
# LangChain Documentation Helper

Follow Eden Marco (Github: emarco177) instruction from Langchain course to create a document assistant

Vectorstore Pinecone Ingestion -> RetrievalQA chain(prompt augmentation) -> "Frontend" with Streamlit -> Memory Management

## Technologies
Langchain
Pinecone
Streamlit(UI)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PINECONE_API_KEY`
`PINECONE_ENVIRONMENT_REGION`
`OPENAI_API_KEY`

## Run Locally

Clone the project

```bash
  git clone "URL"
```

Go to the project directory

```bash
  cd document_assistant
```


Install dependencies

```bash
  pipenv install
```

Start the flask server

```bash
  streamlit run main.py
```


## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```
