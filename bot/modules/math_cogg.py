from queue import Queue
from lib.evaluate_str import evalueatestr

def check(author, content, module, chat_queue: Queue, logger):
    if content.startswith("eval "):
        result = evalueatestr(content[5:])
        if result is None:
            chat_queue.put("An error occured")
            return True
        else:
            chat_queue.put(str(result))
            return True