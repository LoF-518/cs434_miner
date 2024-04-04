from dataclasses import dataclass, field

@dataclass(repr=False, order=True)
class GitHubProject:
    """Class to store GitHub API responses"""
    stargazers_count: int = field(default=0, compare=True)
    name: str = field(default="", compare=False, hash=True)
    url: str = field(default="", compare=False, hash=True)

    def __repr__(self):
        return f"{self.name},{self.url},{self.stargazers_count}"
    
    def iter(self):
        return (self.name, self.url, self.stargazers_count)