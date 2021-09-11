from queue import Queue


def check(author, content, module, chat_queue: Queue, logger):
    if content == "ping":
        chat_queue.put("pong!")
        return True
