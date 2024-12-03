from github import Github
from pathlib import Path
import os
from typing import Dict, List
from loguru import logger
import base64

class GitHubIntegration:
    """Handle GitHub API interactions."""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN not found in environment")
            
        self.gh = Github(self.token)
        self.repo = self.gh.get_repo(f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}")
        self.base_branch = os.getenv("GITHUB_BASE_BRANCH", "main")
        
    async def create_pr(self, pr_data: Dict) -> Dict:
        """Create a GitHub PR from analysis results."""
        try:
            # Create branch
            branch_name = f"{os.getenv('PR_BRANCH_PREFIX', 'fix/')}{pr_data['id']}"
            base_sha = self.repo.get_branch(self.base_branch).commit.sha
            self.repo.create_git_ref(f"refs/heads/{branch_name}", base_sha)
            
            # Create commits
            for change in pr_data["changes"]:
                self._commit_file_change(
                    branch_name,
                    change["file"],
                    change["content"],
                    f"AI: {change['description']}"
                )
            
            # Create PR
            pr = self.repo.create_pull(
                title=pr_data["title"],
                body=pr_data["body"],
                head=branch_name,
                base=self.base_branch,
                draft=os.getenv("PR_DRAFT", "true").lower() == "true"
            )
            
            # Add labels
            if labels := os.getenv("PR_LABELS"):
                pr.add_to_labels(*labels.split(","))
                
            return {
                "pr_number": pr.number,
                "pr_url": pr.html_url,
                "status": "created",
                "branch": branch_name
            }
            
        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            return {
                "error": str(e),
                "status": "failed"
            }
            
    def _commit_file_change(self, branch: str, file_path: str, content: str, message: str):
        """Commit a file change to a branch."""
        try:
            # Get current file if exists
            try:
                current = self.repo.get_contents(file_path, ref=branch)
                self.repo.update_file(
                    file_path,
                    message,
                    content,
                    current.sha,
                    branch=branch
                )
            except:
                # File doesn't exist, create it
                self.repo.create_file(
                    file_path,
                    message,
                    content,
                    branch=branch
                )
        except Exception as e:
            logger.error(f"Failed to commit file {file_path}: {e}")
            raise 