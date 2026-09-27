"""
Project: Relational Blog Platform
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class BlogRepository:
    def __init__(self):
        self.posts = {}
        self.comments = {}
        self.tags = {}

    def create_post(self, post_id: int, title: str, author: str, tags: list[str]) -> dict:
        post = {"id": post_id, "title": title, "author": author, "tags": tags}
        self.posts[post_id] = post
        return post

    def add_comment(self, post_id: int, comment_id: int, text: str):
        if post_id not in self.comments:
            self.comments[post_id] = []
        self.comments[post_id].append({"id": comment_id, "text": text})

    def get_posts_eager(self) -> list[dict]:
        # Eager load: joins comments in a single aggregated batch
        results = []
        for pid, post in self.posts.items():
            item = dict(post)
            item["comments"] = self.comments.get(pid, [])
            results.append(item)
        return results
