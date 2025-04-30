# now pass to the llm chat model to get a answer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBRmB4cyFLIiXWOlyNvm2TpJFsTvFS_ldc"

def get_answer(query,r_doc):
  template="""Use the following pieces of context to answer the question below.
    If you cannot answer, just say that you do not know, do not try to make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
  """
  promt = ChatPromptTemplate.from_template(template)
  output_parser = StrOutputParser()
  llm = ChatGoogleGenerativeAI(
      temperature=0.8,
      model="gemini-2.0-flash",
      max_retries=5
  )

  chain = promt | llm | output_parser
  answer = chain.invoke({
      "context":r_doc,
      "question":query
  })
  return answer
