class MathCogg:
    from queue import Queue
    from bot.lib.evaluate_str import evalueatestr

    def check(self, author, content, chat_queue: Queue, logger):
        if content.startswith("eval "):
            result = self.evalueatestr(content[5:])
            if result is None:
                chat_queue.put("An error occured")
                return True
            else:
                chat_queue.put(str(result))
                return True

module_coggs = [MathCogg]