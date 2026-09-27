from typing import Dict, List, Set

class SocialFeedPlatform:
    def __init__(self, celebrity_threshold: int = 50):
        self.celebrity_threshold = celebrity_threshold
        self.followers: Dict[str, Set[str]] = {}
        self.inbox_feeds: Dict[str, List[str]] = {}
        self.celebrity_posts: Dict[str, List[str]] = {}

    def follow(self, follower: str, followee: str):
        if followee not in self.followers:
            self.followers[followee] = set()
        self.followers[followee].add(follower)

    def post(self, author: str, post_id: str):
        follower_count = len(self.followers.get(author, set()))
        if follower_count >= self.celebrity_threshold:
            # Celebrity: Pull on read (omit write fanout)
            if author not in self.celebrity_posts:
                self.celebrity_posts[author] = []
            self.celebrity_posts[author].append(post_id)
        else:
            # Regular user: Fanout on write (push to inboxes)
            for f in self.followers.get(author, set()):
                if f not in self.inbox_feeds:
                    self.inbox_feeds[f] = []
                self.inbox_feeds[f].append(post_id)

    def get_feed(self, user_id: str) -> List[str]:
        feed = list(self.inbox_feeds.get(user_id, []))
        # Merge celebrity posts from followed accounts
        for author, posts in self.celebrity_posts.items():
            if user_id in self.followers.get(author, set()):
                feed.extend(posts)
        return feed
