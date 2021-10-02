class MovementCogg:
    from config.conf import owner_username
    def __init__(self) -> None:
        pass
    
    def check(self, author, content, chat_queue, logger):
        if content.startswith("move"):
            if self.owner_username in author:
                #chat_queue.put({"move": [("w", 1.0),("a", 1.0), ("s", 1.0), ("d", 1.0)]})
                parts = content[4:].split(" ")[1:]
                if (len(parts) % 2) != 0:
                    chat_queue.put("bad input")
                    return True
                last = None
                instructions = []
                for part in parts:
                    if last is None:
                        last = part
                        continue
                    key = last
                    if key not in ["w", "a", "s", "d", "sp"]:
                        chat_queue.put("bad input")
                        return True 
                    try:
                        duration = float(part)
                        if duration > 10.0:
                            raise ValueError
                    except ValueError:
                        chat_queue.put("bad input")
                        return True
                    instructions.append((key, duration))
                    last = None
                chat_queue.put({"move": instructions})
                return True
            else:
                chat_queue.put("you cannot do that")
                return True
        return False

module_coggs = [MovementCogg]