import json
import base64
from github import Github
from github import GithubException
import os
from datetime import datetime
import streamlit as st

class GitHubStorage:
    """Handle data storage using GitHub API"""
    
    def __init__(self):
        # Try to get secrets from Streamlit Cloud secrets
        try:
            self.token = st.secrets.get("GITHUB_TOKEN")
            self.repo_name = st.secrets.get("GITHUB_REPO")
            self.branch = st.secrets.get("GITHUB_BRANCH", "main")
            self.file_path = st.secrets.get("DATA_FILE_PATH", "progress_data.json")
        except:
            # Fallback to environment variables for local development
            self.token = os.getenv("GITHUB_TOKEN")
            self.repo_name = os.getenv("GITHUB_REPO")
            self.branch = os.getenv("GITHUB_BRANCH", "main")
            self.file_path = os.getenv("DATA_FILE_PATH", "progress_data.json")
        
        self.repo = None
        self.sha = None
        
        if self.token and self.repo_name:
            try:
                self.g = Github(self.token)
                self.repo = self.g.get_repo(self.repo_name)
                # Test connection
                _ = self.repo.name
            except Exception as e:
                st.warning(f"⚠️ GitHub storage not available: {e}. Using local storage only.")
                self.repo = None
        else:
            st.info("💡 GitHub storage not configured. Using local storage only. To enable cloud backup, add GitHub secrets in Streamlit Cloud settings.")
    
    def save_data(self, data):
        """Save data to GitHub"""
        if not self.repo:
            return False
        
        try:
            content = json.dumps(data, indent=2)
            try:
                # Try to get existing file
                contents = self.repo.get_contents(self.file_path, ref=self.branch)
                self.sha = contents.sha
                # Update existing file
                self.repo.update_file(
                    self.file_path,
                    f"Auto-save: Update progress data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    content,
                    self.sha,
                    branch=self.branch
                )
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        self.file_path,
                        f"Auto-save: Initial data save {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        content,
                        branch=self.branch
                    )
                else:
                    raise
            return True
        except Exception as e:
            st.error(f"Error saving to GitHub: {e}")
            return False
    
    def load_data(self):
        """Load data from GitHub"""
        if not self.repo:
            return None
        
        try:
            contents = self.repo.get_contents(self.file_path, ref=self.branch)
            self.sha = contents.sha
            content = base64.b64decode(contents.content).decode('utf-8')
            return json.loads(content)
        except GithubException as e:
            if e.status == 404:
                # File doesn't exist yet
                return None
            else:
                st.error(f"Error loading from GitHub: {e}")
                return None
        except Exception as e:
            st.error(f"Error loading from GitHub: {e}")
            return None
    
    def backup_data(self, data):
        """Create a backup with timestamp"""
        if not self.repo:
            return False
        
        try:
            backup_path = f"backups/progress_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            content = json.dumps(data, indent=2)
            
            try:
                self.repo.create_file(
                    backup_path,
                    f"Backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    content,
                    branch=self.branch
                )
                return True
            except:
                return False
        except:
            return False
    
    def is_available(self):
        """Check if GitHub storage is available"""
        return self.repo is not None

# Initialize GitHub storage
@st.cache_resource
def get_github_storage():
    return GitHubStorage()
