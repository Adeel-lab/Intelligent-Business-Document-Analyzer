from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

def get_answer(question: str, doc_id: str):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    vectorstore = Chroma(
        persist_directory=f"./chroma_db/{doc_id}",
        embedding_function=embeddings
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 15})

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY"),
        max_tokens=1024
    )

    prompt = ChatPromptTemplate.from_template("""
You are a financial analyst assistant analyzing a corporate annual report.
Answer the question below using ONLY the context provided.
Be comprehensive, specific, and structured.
Always cite page numbers like (Page X).
List ALL relevant points you find — do not summarize too briefly.

Context:
{context}

Question: {question}

Provide a detailed, well-structured answer:
""")

    def format_docs(docs):
        return "\n\n".join(
            f"[Page {doc.metadata.get('page', '?')}]: {doc.page_content}"
            for doc in docs
        )

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    answer = chain.invoke(question)
    source_docs = retriever.invoke(question)
    sources = [f"Page {doc.metadata.get('page', '?')}: {doc.page_content[:100]}" for doc in source_docs]

    return answer, sources