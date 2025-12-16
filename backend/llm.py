from langchain_ollama import ChatOllama

llm = ChatOllama(
    # model='gemma3:4b-it-qat',
    model='qwen3:4b-instruct',
    temperature=0,

)