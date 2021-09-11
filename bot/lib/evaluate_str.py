import numexpr as ne
import re
from collections import Counter as count

def evalueatestr(expr):
    expr = str(expr)
    for i in ["__import__", "import", "os", "rm", "sys", "importlib", "__builtins__", "\"", "\'", "subprocess", "eval", "exec"]:
        if i in expr:
            return "nice try"#not for real security, but for lols
    if re.search(r"[a-zA-Z,/;:?\"\'\\|\[\]\{\}]", expr):# prob unecesary, but another pre-check
        return "Illegal charecters in input"
    letters = count(expr)
    if letters["*"] > 40:
        return "Too many multiplications/powers!"
    result = None
    try:
        result = ne.evaluate(str(expr), local_dict={}, global_dict={}).item()
    except KeyError as e:
        pass
    finally:
        return result
