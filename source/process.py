import re
import json
import demjson3
import jstyleson


class SigData:
    def __init__(self, data, text_head, text_data):
        self.data = data
        self.text_head = text_head
        self.text_data = text_data


def parse_sig_file(text: str) -> dict:
    # счет x-ов
    def eval_str(match):
        expr = match.group()
        return str(eval(expr))

    pattern = r"""var\s+lines\s*=\s*lines\s*\|\|\s*\{\};\s*
    lines\s*\[\s*['"].+['"]\s*\]\s*=\s*lines\s*\[\s*['"].+['"]\s*\]\s*\|\|\s*\{\};\s*
    lines\s*\[\s*['"].+['"]\s*\]\s*\[\s*['"]\d+['"]\s*\]\s*=\s*"""

    sig_head = re.match(pattern, text, re.DOTALL | re.VERBOSE)
    if sig_head:
        sig_head = sig_head.group()
        sig_data = re.sub(pattern, '', text, flags=re.DOTALL | re.VERBOSE)
        # считаем иксы для нормального парсинга
        sig_data = re.sub(r"(?<=x: ).+?(?=,)", eval_str, sig_data)
    else:
        sig_data = None
    try:
        parsed = demjson3.decode(sig_data)
    except demjson3.JSONDecodeError:
        parsed = None

    sig_data = {
        'data': parsed,
        'text': {
            'head': sig_head,
            'rawdata': sig_data,
        },
    }
    sig_data = SigData(parsed, sig_head, sig_data)
    return sig_data


def data_to_file(sig_data: SigData) -> str:
    text = sig_data.text_head + json.dumps(sig_data.data, indent=4, ensure_ascii=False)
    return text