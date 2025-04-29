import logging
import os
from datetime import datetime

# ✅ Create logger folder with today's date (YYYY-MM-DD)
today = datetime.now().strftime("%Y-%m-%d")
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", today))
os.makedirs(log_dir, exist_ok=True)
log_file_path = os.path.join(log_dir, "app.log")

# ✅ Create logger instance
logger = logging.getLogger("BrainLogs")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent double logging if root logger is used elsewhere

# ✅ Formatter (same for both file & console)
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ✅ File handler
file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ✅ Console (stream) handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ✅ Function to access logger
def get_logger(name: str = __name__):
    return logger

__all__ = ["get_logger"]
