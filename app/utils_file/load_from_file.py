import os
import json
from Brain.DataLoader.DocumentLoader import DocumentLoader
from Brain.DataLoader.WebLoader import WebLoader
from Logger.logger import logger

def load_from_file(entry):
    try:
        if os.path.basename(entry.path) == "weblinks.json":
            with open(entry.path,"r",encoding="utf-8") as f:
                data = json.load(f)
                all_docs = []
                for item in data:
                    link = item.get("link")
                    follow = item.get("follow", False)
                    depth = item.get("depth", 1)
                    loader = WebLoader(link, follow, depth)
                    logger.info(f"loading from link {link}")
                    docs = loader.load()
                    all_docs.extend(docs)
                return all_docs

        else:
            loader = DocumentLoader(entry.path)
            logger.info(f"loading file from {entry.path}")
            return loader.load()
    except Exception as e:
        loader.error(f"Error loading {entry.path}: {e}")
        return []
