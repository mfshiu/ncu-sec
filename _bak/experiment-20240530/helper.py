import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import re
from pathlib import Path
import psycopg2

from abdi_config import LOGGER_NAME


with open("./app_config.json", 'r') as file:
    __app_config = json.load(file)

__logger = logging.getLogger(LOGGER_NAME)
__log_init = False


def get_config():
    return __app_config


def find_deepest(key, dictionary, depth=0):
    deepest_value = None
    max_depth = -1

    if key in dictionary:
        deepest_value = dictionary[key]
        max_depth = depth

    for subkey, subvalue in dictionary.items():
        if isinstance(subvalue, dict):  # Only search in sub-dictionaries
            found_value, found_depth = find_deepest(key, subvalue, depth + 1)
            if found_depth > max_depth:
                deepest_value = found_value
                max_depth = found_depth

    return deepest_value, max_depth


def out(text:str):
    if os.name == 'nt':
        text = text.encode('cp950', "ignore")
        text = text.decode('cp950')
    return text


def ensure_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        __logger.info(f"Directory '{dir_path}' created successfully.")
    
    
def get_logger():
    global __log_init
    global __logger
    
    if not __log_init:
        __log_init = True
        
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR
        }
        cfg = __app_config
        log_level = logging.DEBUG
        if "log_level" in cfg:
            if cfg["log_level"] in log_levels:
                log_level = log_levels[cfg["log_level"]]            
            __logger = _init_logging(cfg.get("log_path"), log_level)
        
    return __logger


def _init_logging(log_path:str, log_level):
    formatter = logging.Formatter(
        '%(levelname)1.1s %(asctime)s %(module)15s:%(lineno)03d %(funcName)15s) %(message)s',
        datefmt='%H:%M:%S')
    
    Path(os.path.dirname(log_path)).mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(log_path, when="d", encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    global __logger
    __logger.addHandler(console_handler)
    __logger.addHandler(file_handler)    
    __logger.setLevel(log_level)

    return __logger


def remove_emojis(text):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F700-\U0001F77F"  # alchemical symbols
                           u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                           u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                           u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                           u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                           u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                           u"\U00002702-\U000027B0"  # Dingbat symbols
                           u"\U000024C2-\U0001F251"  # Enclosed characters
                           "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', text)



######################
# Database Operation #
######################


def create_connection():
    return psycopg2.connect(**__app_config['db_params'])
# def create_connection():
#     conn = None
#     try:
#         conn = psycopg2.connect(**__app_config['db_params'])
#     except psycopg2.Error as ex:
#         __logger.exception(ex)
        
#     return conn



def execute_command(command, params):
    # __logger.debug(f"command: {command}\nparams:{params}")
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(command, params)
        conn.commit()
    except Exception as ex:
        __logger.exception(ex)
    finally:
        if conn:
            cursor.close()
            conn.close()


# command_params: [(command, params), (command, params)...]
def execute_commands(command_params:list):
    conn = create_connection()
    try:
        cursor = conn.cursor()
        for pair in command_params:
            command, params = pair[0], pair[1]
            # print(f"command: {command}, params: {params}")
            cursor.execute(command, params)
        conn.commit()
    except Exception as ex:
        conn.rollback()
        raise ex
    finally:
        cursor.close()
        conn.close()
  

def insert_and_fetch_id(command, params):
    __logger.debug(f"command: {command}\nparams:{params}")
    identity_id = None
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(command, params)
        conn.commit()
        identity_id = cursor.fetchone()[0]
    except Exception as ex:
        __logger.exception(ex)
    finally:
        if conn:
            cursor.close()
            conn.close()

    return identity_id


def query(query, params=None):
    conn = create_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
        
    return rows
  

def query_column(query, params=None):
    conn = create_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        values = [row[0] for row in rows]
    finally:
        cursor.close()
        conn.close()
        
    return values


def query_scalar(query, params=None):
    conn = create_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        scalar = result[0] if result else None
    finally:
        cursor.close()
        conn.close()
        
    return scalar
  

def query_as_dict_list(query, params=None):
    conn = create_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()

        col_names = [desc[0] for desc in cur.description]
        data_as_dict_list = []
        for row in rows:
            data_as_dict_list.append({col_names[i]: row[i] for i in range(len(col_names))})
            
    except Exception as ex:
        __logger.exception(ex)
        data_as_dict_list = []
        
    finally:
        cur.close()
        conn.close()
        
    return data_as_dict_list