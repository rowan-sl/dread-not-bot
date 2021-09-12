class DebugCogg:
    def __init__(self) -> None:
        pass
    def check(self, author, content, chat_queue, logger):
        if content == "ping":
            chat_queue.put("pong!")
            return True

module_coggs = [DebugCogg]
