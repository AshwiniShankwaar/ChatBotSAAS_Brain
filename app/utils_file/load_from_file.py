import logging
import os
import json
from Brain.DataLoader.DocumentLoader import DocumentLoader
from Brain.DataLoader.WebLoader import WebLoader
from Logger import logger

def load_from_file(entry,botlogger:logging.Logger):
    try:
        base_name = os.path.basename(entry.path)
        if base_name == "weblinks.json":
            with open(entry.path,"r",encoding="utf-8") as f:
                data = json.load(f)
                all_docs = []
                for idx,item in enumerate(data):
                    link = item.get("link")
                    follow = item.get("follow", False)
                    depth = item.get("depth", 1)
                    loader = WebLoader(link, follow, depth)
                    botlogger.info(f"loading from link {link}")
                    docs = loader.load()
                    for i,doc in enumerate(docs):
                        doc.metadata['source']=link
                        doc.metadata['type'] = "weblink"
                        doc.metadata['index'] = f"{idx}-{i}"
                    all_docs.extend(docs)
                return all_docs

        else:
            loader = DocumentLoader(entry.path)
            docs = loader.load()
            botlogger.info(f"loading file from {entry.path}")
            for i,doc in enumerate(docs):
                doc.metadata['source'] = base_name
                doc.metadata['type'] = "file"
                doc.metadata['index'] = i
            return docs
    except Exception as e:
        loader.error(f"Error loading {entry.path}: {e}")
        return []
