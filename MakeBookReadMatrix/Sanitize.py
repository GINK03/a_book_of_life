
import mojimoji
import re

def sanitize(x):
    x = x.lower()
    x = mojimoji.han_to_zen(x)
    x = mojimoji.zen_to_han(x, kana=False)
    x = re.sub(r'\(.*?\)', '', x)
    x = re.sub(r'〈.*?〉', '', x)
    x = re.sub(r'\s{1,}', ' ', x)
    x = x.strip()
    x = re.sub(r'\d{1,}$', '', x)
    x = re.sub(r'(第|\s)\d{1,}(巻|集)', '', x)
    x = x.strip()
    x = re.sub(r'\)', '', x)
    x = re.sub(r'\[.*?\]', '', x)
    x = re.sub(r'\【.*?】', '', x)
    x = re.sub(r'\s―\s', ' ', x)
    x = re.sub(r':\s', ' ', x)
    x = x.strip()
    x = re.sub(r'\s{1,}', ' ', x)
    return x
