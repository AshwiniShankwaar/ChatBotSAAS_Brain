# now pass to the llm chat model to get a answer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from typing import Optional
load_dotenv()


def get_answer(query,r_doc,agent_role,past_conversation:Optional[dict[str]]=None):
  template="""
    you are a {agent} agent
    Use the following pieces of context to answer the question below.
    If you cannot answer, just say that you do not know, do not try to make up an answer.

    Context:
    {context}

    Past conversation:
    {past_chat}
    
    Question:
    {question}

    Answer:
  """
  promt = ChatPromptTemplate.from_template(template)
  output_parser = StrOutputParser()
  llm = ChatGoogleGenerativeAI(
      temperature=0.8,
      model = os.getenv("LLM_MODEL"),
      max_retries = 5
  )

  chain = promt | llm | output_parser
  answer = chain.invoke({
      "agent":agent_role,
      "context":r_doc,
      "past_chat":past_conversation,
      "question":query
  })
  return answer
