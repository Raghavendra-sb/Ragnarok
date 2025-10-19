# flake8: noqa
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI



client = OpenAI(
    # API key for the OpenAI client using the Google base URL
    api_key=os.getenv("GEMINI_API_KEY") ,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    # API key for the LangChain GoogleGenerativeAIEmbeddings
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# Connect to Qdrant service defined in docker-compose.yaml
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://vector-db:6333",
    collection_name="learning_vectors",
    embedding=embedding_model,
)


def process_query(query: str):
    """
    Processes a user query: performs RAG search, constructs context, and generates a response.
    """
    print(f"Searching chunks for: {query}")

    # 1. RAG Search
    search_results = vector_db.similarity_search(
        query=query
    )

    context = "\n\n".join(
        [
            f"Page Content: {result.page_content}\nPage Number: {result.metadata.get('page_label', 'N/A')}\nFile Location: {result.metadata.get('source', 'N/A')}"
            for result in search_results
        ]
    )

    # 2. System Prompt Construction
    SYSTEM_PROMPT = f"""
        You are a helpful AI assistant who answers user query based on the available context retrieved from a PDF file along with page_contents and page number.

        You should only answer the user based on the following context and navigate the user to open the right page number to know more.

        Context:
        {context}
    """

    # 3. Call Gemini Chat Completion via OpenAI client
    chat_completion = client.chat.completions.create(
        model="gemini-2.5-flash", # <--- FIX: Changed model name from gemini-2.0-flash
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ],
    )

    response_content = chat_completion.choices[0].message.content

    # 4. Save/Log Result (Assuming this is just a print statement for now)
    print("--- JOB COMPLETE ---")
    print(f"User Query: {query}")
    print(f"AI Response: {response_content}\n\n\n")

    return response_content
