# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# texts = text_splitter.split_documents(all_docs)

# embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# mongo_client = MongoClient(os.getenv("MONGO_URI"))
# collection = mongo_client["FinancialAdvisor"]["chunks"]

# vector_store = MongoDBAtlasVectorSearch.from_documents(
#     documents=texts,
#     collection=collection,
#     embedding=embedding_model,
#     index_name="vector_index",
# )
