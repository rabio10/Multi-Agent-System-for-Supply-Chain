# logging_config.py
import logging
import datetime
import os
from rich.logging import RichHandler

FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
LOG_DIR = "logs"
LOG_FILE = "log-{datetime.datetime.now().strftime('%Y-%m-%d')}.log"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# create logs folder
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = f"logs/log-{datetime.datetime.now().strftime('%m-%d-%Y %H-%M-%S')}.log"
# one time log config
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        RichHandler(rich_tracebacks=True, markup=True, show_time=True, show_path=False),
        logging.FileHandler(log_filename, mode='w', delay=False)
    ],
    force=True
)

log = logging.getLogger("rich")

# Force immediate output
for handler in log.handlers:
    handler.flush()

