from collections import defaultdict
import time
from config import RATE_LIMIT_MINUTES, MAX_REQUESTS_PER_USER

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def can_make_request(self, user_id: int) -> bool:
        """
        Check if a user can make a request based on their rate limit.
        """
        current_time = time.time()
        # Remove expired timestamps
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if current_time - timestamp < RATE_LIMIT_MINUTES * 60
        ]
        
        # Check if user has exceeded rate limit
        return len(self.requests[user_id]) < MAX_REQUESTS_PER_USER
    
    def add_request(self, user_id: int):
        """
        Record a new request for the user.
        """
        self.requests[user_id].append(time.time())
    
    def get_remaining_requests(self, user_id: int) -> int:
        """
        Get the number of remaining requests for a user.
        """
        if self.can_make_request(user_id):
            return MAX_REQUESTS_PER_USER - len(self.requests[user_id])
        return 0
