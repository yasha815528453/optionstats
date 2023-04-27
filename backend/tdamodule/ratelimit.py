import time

class RateLimiter:
    def __init__(self, rate_limit, time_window):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_time = []

    def get_token(self):
        now = time.time()
        self.request_time = [t for t in self.request_time if t > now - self.time_window]
        if len(self.request_time) < self.rate_limit:
            self.request_time.append(now)
            return True
        else:
            return False
