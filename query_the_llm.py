import argparse
from get_embadding_func import get_embedding
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_cohere.llms import Cohere
from dotenv import load_dotenv
import os

load_dotenv()

# the prompt llm will follow
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}

If the question or answer is out of context, respond with: no data found within given context.
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)



def query_rag(query_text: str):
    embedding_function = get_embedding()
    db = Chroma(persist_directory='chroma', embedding_function=embedding_function)

    # similarity search will churn out 5 most relevent search from vector db as k value is 5
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    cohere = Cohere(cohere_api_key=os.environ.get("API_KEY"))
    response_text = cohere.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results] # it will include metadata like page number and pdf in response
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
