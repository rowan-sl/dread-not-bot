class RandomCogg:
    #put import statements here
    import secrets
    import string
    def __init__(self):
        pass
    
    def check(self, author, content: str, chat_queue, logger):
        if content.startswith("randombullshitgo"):
            chat_queue.put("".join([self.secrets.choice(self.string.ascii_letters) for x in range(299)]))
        return True

module_coggs = [RandomCogg]