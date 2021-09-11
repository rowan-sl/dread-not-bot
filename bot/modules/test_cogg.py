from queue import Queue


def check(author, content, module, chat_queue: Queue, logger):
    # returns True if sucessfull, else returns false.
    # adds its things to output queue on its own
    chat_queue.put("testing 1 2 3")
    return True
    