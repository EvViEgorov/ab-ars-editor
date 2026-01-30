import re
import demjson3


def parse_sig_file(text: str, text_only=False):
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

    parsed = demjson3.decode(sig_data)
    if text_only:
        return sig_head, sig_data
    else:
        return parsed