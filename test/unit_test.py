from fastapi import UploadFile
from io import BytesIO
import os
from app.utils_file.files import save_data
def create_fake_upload_file_from_path(file_path: str) -> UploadFile:
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
    return UploadFile(filename=filename, file=BytesIO(content))


def test_save_data_creates_files_and_weblinks():
    client_id = "testclient"
    chatbot_id = "testbot"

    # Use real test files from local folder
    files = [
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\concepts.pdf"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\developers-guide.pdf"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\plsqlLearning.txt"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\json_schema.json"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Desktop\\projects\\angleApiTrading\\data\\bse_20241201TO20241224.csv")
    ]

    weblinks = {
        "links": [
            {"link": "https://python.langchain.com/docs/introduction/", "follow": True, "depth": 2},
            {"link": "https://langchain-ai.github.io/langgraph/tutorials/introduction/", "follow": True, "depth": 1}
        ]
    }

    result_path = save_data(client_id, chatbot_id, files, weblinks)

    assert os.path.exists(result_path)
    for f in files:
        assert os.path.exists(os.path.join(result_path, f.filename))

    weblink_path = os.path.join(result_path, "weblinks.json")
    assert os.path.exists(weblink_path)

