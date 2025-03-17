from langchain_community.llms import OpenAI
from config import OPENAI_API_KEY

class QueryRewriter:
    def __init__(self):
        self.llm = OpenAI(api_key=OPENAI_API_KEY)

    def rewrite_query(self, user_query):
        prompt = f"Rewrite the following search query to be more precise and effective:\n\n'{user_query}'"
        response = self.llm.invoke(prompt)
        return response.strip()
if __name__ == "__main__":
    rewriter = QueryRewriter()
    user_query = input("Enter a search query: ")
    optimized_query = rewriter.rewrite_query(user_query)
    print(f"Optimized Query: {optimized_query}")
