import os
import logging
from datetime import datetime

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/system_run_{datetime.now().strftime('%Y%m%d')}.log"
    
    logger = logging.getLogger("FinDashPro")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()
        
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    return logger