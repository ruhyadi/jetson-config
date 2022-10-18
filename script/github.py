"""
Github API management
"""

import os
import json
import git
import requests
import dotenv
import time

dotenv.load_dotenv()

class GitAPI:
    def __init__(self, username, token):
        self.username = username
        self.token = token

        # header for github api
        self.header = {
            "Authorization": "token " + self.token,
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/octet-stream"
        }

    def clone(self, repo: str, path: str, ref: str = None):
        """Clone a repository with authentication"""
        url = f"https://{self.username}:{self.token}@github.com/{self.username}/{repo}.git"
        self.repo = git.Repo.clone_from(url=url, to_path=path)
        self.repo.git.checkout(ref) if ref else None
        
        print(f"[INFO] Cloned {self.username}/{repo} to {path}")

    def create_release(self, repo: str, tag_name: str, name: str, body: str):
        """Create a release on github"""
        url = f"https://api.github.com/repos/{self.username}/{repo}/releases"
        data = {
            "tag_name": tag_name,
            "name": name,
            "body": body
        }

        r = requests.post(url=url, headers=self.header, data=json.dumps(data))
        if r.status_code == 201:
            print(f"[INFO] Created release {name} on {self.username}/{repo}")
            print(f"[INFO] Release ID: {r.json()['id']}")
            print(f"[INFO] Release URL: {r.json()['html_url']}")
        else:
            print(f"[ERROR] Failed to create release {name} on {self.username}/{repo}")

        # wait for release to be created
        time.sleep(2)

    def push_assets(self, repo: str, tag: str, assets: list):
        """Push assets to a release on github"""
        releases = self.list_releases(repo=repo)
        release_id = releases[tag]

        for asset in assets:
            url = f"https://uploads.github.com/repos/{self.username}/{repo}/releases/{release_id}/assets?name={asset.split('/')[-1]}"
            with open(asset, "rb") as f:
                r = requests.post(url=url, headers=self.header, data=f)
                if r.status_code == 201:
                    print(f"[INFO] Uploaded {asset} to {self.username}/{repo}")
                else:
                    print(f"[ERROR] Failed to upload {asset} to {self.username}/{repo}")

    def get_assets(self, repo: str, tag: str, path: str):
        """Download assets from github release"""
        releases = self.list_releases(repo=repo)
        release_id = releases[tag]

        url = f"https://api.github.com/repos/{self.username}/{repo}/releases/{release_id}/assets"
        r = requests.get(url=url, headers=self.header)
        if r.status_code == 200:
            for asset in r.json():
                asset_url = asset["browser_download_url"]
                asset_name = asset["name"]
                asset_path = os.path.join(path, asset_name)
                
                with open(asset_path, "w") as f:
                    r = requests.get(url=asset_url)
                    f.write(r.content)
                    print(f"[INFO] Downloaded {asset_name} to {asset_path}")
        else:
            print(f"[ERROR] Failed to download assets from {self.username}/{repo}")

    def list_releases(self, repo: str, output: bool = False):
        """List releases on github"""
        print(f"\n[INFO] Listing releases on {self.username}/{repo}") if output else None
        url = f"https://api.github.com/repos/{self.username}/{repo}/releases"

        r = requests.get(url=url, headers=self.header)
        if r.status_code == 200:
            if output:
                print(f"[INFO] Releases on https://github.com/{self.username}/{repo}")
                for release in r.json():
                    print(f"\n[INFO] Release Tag: {release['tag_name']}")
                    print(f"[INFO] Release ID: {release['id']}")
                    print(f"[INFO] Release URL: {release['html_url']}")
        else:
            print(f"[ERROR] Failed to list releases on {self.username}/{repo}")

        return {release["tag_name"]: release["id"] for release in r.json()}

    def delete_release(self, repo: str, tag: str, include_tag: bool = False):
        """Delete a release on github"""
        releases = self.list_releases(repo=repo)
        release_id = releases[tag]

        url = f"https://api.github.com/repos/{self.username}/{repo}/releases/{release_id}"

        r = requests.delete(url=url, headers=self.header)
        if r.status_code == 204:
            print(f"[INFO] Deleted release {tag} on {self.username}/{repo}")
        else:
            print(f"[ERROR] Failed to delete release {tag} on {self.username}/{repo}")

        if include_tag:
            self.delete_tag(repo=repo, tag=tag)

    def delete_tag(self, repo: str, tag: str):
        """Delete a tag on github"""
        url = f"https://api.github.com/repos/{self.username}/{repo}/git/refs/tags/{tag}"

        r = requests.delete(url=url, headers=self.header)
        if r.status_code == 204:
            print(f"[INFO] Deleted tag {tag} on {self.username}/{repo}")
        else:
            print(f"[ERROR] Failed to delete tag {tag} on {self.username}/{repo}")

if __name__ == "__main__":

    client = GitAPI(username="ruhyadi", token=os.environ["GITHUB_TOKEN"])
    # client.clone(repo="jetson-config", path="test")
    # client.create_release(
    #     repo="jetson-config",
    #     tag_name="v0.1.0",
    #     name="v0.1.0",
    #     body="Initial release"
    # )
    # client.list_releases(repo="jetson-config")
    # client.delete_release(repo="jetson-config", tag="v0.1.0", include_tag=True)
    # client.push_assets(
    #     repo="jetson-config",
    #     tag="v0.1.0",
    #     assets=["README.md", "LICENSE"]
    # )

    client.get_assets(
        repo="jetson-config",
        tag="v0.1.0",
        path="test"
    )
