class RandomCogg:
    #put import statements here
    from bot.lib.randomstring import randomstr
    def __init__(self):
        pass
    
    def check(self, author, content: str, chat_queue, logger):
        if content.startswith("randomgarbage"):
            chat_queue.put(self.randomstr(299))
        return True

module_coggs = [RandomCogg]