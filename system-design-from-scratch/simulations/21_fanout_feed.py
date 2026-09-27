from typing import Dict, List, Set

class HybridFeedService:
    def __init__(self, celebrity_threshold: int = 100):
        self.celebrity_threshold = celebrity_threshold
        self.followers: Dict[str, Set[str]] = {}
        self.inbox_feeds: Dict[str, List[str]] = {}
        self.user_posts: Dict[str, List[str]] = {}

    def follow(self, follower: str, followee: str):
        if followee not in self.followers:
            self.followers[followee] = set()
        self.followers[followee].add(follower)

    def post_message(self, author: str, post_id: str):
        if author not in self.user_posts:
            self.user_posts[author] = []
        self.user_posts[author].append(post_id)

        # Fanout on write for regular users
        followers = self.followers.get(author, set())
        if len(followers) <= self.celebrity_threshold:
            for f in followers:
                if f not in self.inbox_feeds:
                    self.inbox_feeds[f] = []
                self.inbox_feeds[f].append(post_id)
