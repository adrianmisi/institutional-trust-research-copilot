class Retriever:
    def __init__(self, vectorstore, k: int = 5):
        self.vectorstore = vectorstore
        self.k = k
        
    def get_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k": self.k})
