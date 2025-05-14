# now pass to the llm chat model to get a answer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from typing import Optional
from Logger import get_logger
logger = get_logger()
load_dotenv()


def get_answer(query,r_doc,agent_role,past_conversation:Optional[dict[str]]=None):
  # logger.info("from line 14 of answer_generated ")
  # logger.info(r_doc)
  template="""
    you are a {agent} agent
    Use the following pieces of context to answer the question below.
    If you cannot answer, just say that you do not know , do not try to make up an answer also
    dont tell the source directly.

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

  chain = promt | llm
  #{'input_tokens': 80, 'output_tokens': 41, 'total_tokens': 121, 'input_token_details': {'cache_read': 0}}
  answer = chain.invoke({
      "agent":agent_role,
      "context":r_doc,
      "past_chat":past_conversation,
      "question":query
  })
  logger.info(answer.usage_metadata)
  #here the 80 represent the token that is get as a static prompt and added to the query and
  # create a prompt to generate a anser
  input_tokens = max(0, answer.usage_metadata['input_tokens'] - 80)
  output_tokens = answer.usage_metadata['output_tokens']
  usages_data={
      "input_tokens": input_tokens,
      "output_tokens": output_tokens,
      "total_tokens": input_tokens+output_tokens
  }
  answer = output_parser.invoke(answer.content)
  return answer,usages_data
