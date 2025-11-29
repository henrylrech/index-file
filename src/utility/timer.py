import time

class Timer:
    def __init__(self):
        self.start_time = time.time()

    def seconds(self):
        if self.start_time is None:
            return ""
        elapsed_time = time.time() - self.start_time
        return f"{elapsed_time:.2f}"
    
    def reset(self):
        """Reinicia o timer para zero."""
        self.start_time = time.time()
