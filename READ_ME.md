## Run the server using uvicorn
```
uvicorn app.Main:app --reload --port 8080
```
port is optional and same way you can even add host to it as well

### Endpoints
There are three end points:
1) ```/chatbot/create_chatbot```
 
This endpoint perorm the work of creating the chatbot:

argu: 
     
     -> payload_data (string)
     -> files (list of files)
     -> weblinks_str (string)

- **payload_data** takes a json in form of string. The value should be in this format.

```
{ 
  "client_id": "test_client", 
  "chatbot_id": "test_bot", 
  "chatbot_name": "TestBot", 
  "chatbot_description": "Test chatbot", 
  "agent_role": "helper", 
  "temprature": 0.5
}
```
Before sending the data check if the chatbot is available or
not in db and also dont allow dublicate chatbot to be created
as it need to be doen in the java backend.

- **files** files takes a list of files. Allowed file format are .pdf, .txt, .csv, .json

- **weblinks_str** takes a json in form of string were the json contains the dict of string.
it should follow the following format.
```
[
  {
    "link": "https://python.langchain.com/docs/introduction/", 
    "follow": true, 
    "depth": 2
  },
  {
    "link": "https://langchain-ai.github.io/langgraph/tutorials/introduction/", 
    "follow": true, 
    "depth": 1
  }
]

```
weblinks_str can be null.

**namespace** will be defined using the client_id and chatbot_id so no dublicate chatbot allowed
chatbot Brain will not store the file it will delete all the file once the chatbot is created.
Logs realted to a chatbot is saved in seprated file so it will be easy to see the logs.

2) ```/query/ask```

This end points is used to ask the question where it will use hybrid search in the background to retrive the data once the data is been retrived it will pass to the llm for proper answer generation

args:
    
    -> payload_data (str)

**payload_data** this will take json data in a string format. In the form the following format.

```
{
        "query":"What is uim",
        "past_msg":null,
        "client_id":"test_client",
        "chatbot_id":"test_bot",
        "agent_role":"helper"
}

- with previous chat
{
    "query": "What is uim",
    "past_msg": [
        {"user": "Hi"},
        {"ai": "Hi, there"}
    ],
    "client_id": "test_client",
    "chatbot_id": "test_bot",
    "agent_role": "helper"
}

```
where past_msg is the list of dist(str,str) 
```
[
    {'user':'example'},
    {'ai':'...'}
]
```

3) ```/health```