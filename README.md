RAG demo in python
vector db - chroma
model - Cohere embading and Cohere from langchain community

Steps to run this project

First install all necessary python libraries listed below - run ( pip install {library_name} )

* langchain_cohere
* langchain_text_splitters
* langchain
* langchain_community

Create a .env file and add in
API_KEY="your cohere api key"

* Add a pdf file as knowldge base in data folder (you will find a existing pdf, can remove it or keep it)
* Run python populate_data.py
* Run python query_the_llm "your question to the llm"

  Example : python3 query_the_llm.py "What are the Disadvantages of tumblers"

  Pre-requisite: squalite >=3.35
  python 3.10
