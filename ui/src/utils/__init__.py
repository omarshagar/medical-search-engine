import os
import pathlib
from pickle import FALSE

from PIL import Image

import pytz
from datetime import datetime


def parse_filename(path: str):
    
    filename = os.path.splitext(os.path.split(path)[-1])[0]
    
    return filename

def type_to_name(specialized_quest_type: str):
    
    sep = ['-', '_', ' ']

    sstr = [*specialized_quest_type]
    
    sstr[0] = sstr[0].upper()
    
    for i in range(1, len(sstr)):
        
        if sstr[i - 1] in sep:
            
            sstr[i - 1] = ' '
            sstr[i] = sstr[i].upper()

        else:
            
            sstr[i] = sstr[i].lower()
    
    return ''.join(sstr)

def is_file(path: str) -> bool:

    return pathlib.Path(path).is_file()

### This function should be modified later
def is_image(path):
        
    if not is_file(path):
        
        return False
    
    try:
        # inefficient and may fail in many cases
        image = Image.open(path)
        del image
        
        return True
    
    except:
        
        return False

def get_utc_time():
    
    date = datetime.utcnow().replace(tzinfo=pytz.utc)
    
    return date

def local_time_format(date: datetime):
    
    return date.astimezone().strftime("%d/%b/%Y,%I:%M:%S %p").split(',')

def get_timedelta(start_date: datetime, in_seconds=False):
        
    current_date = get_utc_time()
    delta = current_date - start_date
    
    return delta.total_seconds() if in_seconds else delta

def timedelta_format(start_date: datetime):
    
    delta = get_timedelta(start_date, in_seconds=False)
    
    if delta.days > 7:
                
        return None, True
        
    elif delta.days != 0:
        
        return f'{delta.days} Days Ago', False
    
    elif delta.seconds > 60 != 0:
        
        return f'{delta.seconds // 60} Minutes Ago', False
    
    else:
        
        return f'{delta.seconds} Seconds Ago', False