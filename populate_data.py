from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_community.vectorstores import Chroma
# import shutil
from get_embadding_func import get_embedding

def loadDoc():
    loader = PyPDFLoader("data/mixing.pdf")
    pages = loader.load()
    return pages

def split_documents(document: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    # splitting the document in format of metadata and Pagecontent.
    return text_splitter.split_documents(document)

def add_to_chroma(chunks: list[Document]):
    db = Chroma(
        persist_directory="chroma", embedding_function=get_embedding()
    )

    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("No new documents to add")


def calculate_chunk_ids(chunks):
    # This will create IDs like "data/monopoly.pdf:6:2"
    # to have a unique id in our metadata the key would be:   Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increase the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Adding it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

document = loadDoc()
split_chunks = split_documents(document)
""" shutil.rmtree('chroma') """ # uncomment this and import shutil from above in case you want to clear out db
add_to_chroma(split_chunks)