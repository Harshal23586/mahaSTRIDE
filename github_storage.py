import json
import base64
from github import Github, GithubException
import os
from datetime import datetime
import streamlit as st

class GitHubStorage:
    """Handle data storage using GitHub API - Supports multiple data files"""
    
    # Define all data files used by the application
    DATA_FILES = {
        "progress": "coordinator_progress_data.json",
        "assignments": "assignments_data.json",
        "custom_tasks": "custom_tasks_data.json",
        "attendance": "attendance_data.json"
    }
    
    def __init__(self):
        # Try to get secrets from Streamlit Cloud secrets
        try:
            self.token = st.secrets.get("GITHUB_TOKEN")
            self.repo_name = st.secrets.get("GITHUB_REPO")
            self.branch = st.secrets.get("GITHUB_BRANCH", "main")
            self.data_prefix = st.secrets.get("DATA_FILE_PREFIX", "data/")
        except:
            # Fallback to environment variables for local development
            self.token = os.getenv("GITHUB_TOKEN")
            self.repo_name = os.getenv("GITHUB_REPO")
            self.branch = os.getenv("GITHUB_BRANCH", "main")
            self.data_prefix = os.getenv("DATA_FILE_PREFIX", "data/")
        
        self.repo = None
        self.file_shas = {}  # Store SHA for each file
        
        if not self.token:
            st.info("💡 GitHub token not configured. Add GITHUB_TOKEN in secrets for cloud backup.")
            return
        
        if not self.repo_name:
            st.info("💡 GitHub repository not configured. Add GITHUB_REPO in secrets (format: username/repo-name)")
            return
        
        try:
            self.g = Github(self.token)
            # Test authentication
            user = self.g.get_user()
            st.success(f"✅ Authenticated as: {user.login}")
            
            # Try to get the repository
            try:
                self.repo = self.g.get_repo(self.repo_name)
                st.success(f"✅ Connected to repository: {self.repo_name}")
                self._ensure_data_directory()
            except GithubException as e:
                if e.status == 404:
                    st.error(f"❌ Repository '{self.repo_name}' not found. Please create it first.")
                    st.info("📝 To fix: Create a repository at https://github.com/new and update GITHUB_REPO secret")
                else:
                    st.error(f"❌ GitHub error: {e}")
                self.repo = None
                
        except Exception as e:
            st.error(f"❌ GitHub connection error: {e}")
            self.repo = None
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists in the repository"""
        if not self.repo:
            return
        
        try:
            # Try to get the data directory
            self.repo.get_contents(self.data_prefix, ref=self.branch)
        except GithubException as e:
            if e.status == 404:
                # Create a .gitkeep file to create the directory
                try:
                    self.repo.create_file(
                        f"{self.data_prefix}.gitkeep",
                        f"Create data directory for storing progress data",
                        "",
                        branch=self.branch
                    )
                except:
                    pass  # Directory might already exist
            # Ignore other errors
    
    def _get_full_path(self, file_key):
        """Get full path for a data file"""
        if file_key in self.DATA_FILES:
            return f"{self.data_prefix}{self.DATA_FILES[file_key]}"
        return f"{self.data_prefix}{file_key}"
    
    def save_data(self, data, file_key="progress"):
        """Save data to GitHub for a specific file"""
        if not self.repo:
            return False
        
        try:
            file_path = self._get_full_path(file_key)
            content = json.dumps(data, indent=2, default=str)
            
            try:
                # Try to get existing file
                contents = self.repo.get_contents(file_path, ref=self.branch)
                self.file_shas[file_key] = contents.sha
                # Update existing file
                self.repo.update_file(
                    file_path,
                    f"Auto-save: Update {file_key} data {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    content,
                    self.file_shas[file_key],
                    branch=self.branch
                )
                return True
            except GithubException as e:
                if e.status == 404:
                    # File doesn't exist, create it
                    self.repo.create_file(
                        file_path,
                        f"Auto-save: Initial {file_key} data save {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                        content,
                        branch=self.branch
                    )
                    return True
                else:
                    raise
        except Exception as e:
            st.error(f"Error saving to GitHub ({file_key}): {e}")
            return False
    
    def load_data(self, file_key="progress"):
        """Load data from GitHub for a specific file"""
        if not self.repo:
            return None
        
        try:
            file_path = self._get_full_path(file_key)
            contents = self.repo.get_contents(file_path, ref=self.branch)
            self.file_shas[file_key] = contents.sha
            content = base64.b64decode(contents.content).decode('utf-8')
            return json.loads(content)
        except GithubException as e:
            if e.status == 404:
                # File doesn't exist yet
                return None
            else:
                return None
        except Exception as e:
            return None
    
    def save_all_data(self, data_dict):
        """Save multiple data files at once"""
        success = True
        for file_key, data in data_dict.items():
            if not self.save_data(data, file_key):
                success = False
        return success
    
    def load_all_data(self):
        """Load all data files"""
        all_data = {}
        for file_key in self.DATA_FILES.keys():
            data = self.load_data(file_key)
            if data is not None:
                all_data[file_key] = data
        return all_data
    
    def backup_data(self, data_dict=None):
        """Create a backup of all data files with timestamp"""
        if not self.repo:
            return False
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_prefix = f"backups/{timestamp}/"
            
            # If specific data provided, backup only that
            if data_dict:
                files_to_backup = data_dict
            else:
                # Load all current data
                files_to_backup = {}
                for file_key in self.DATA_FILES.keys():
                    data = self.load_data(file_key)
                    if data is not None:
                        files_to_backup[file_key] = data
            
            # Create backup directory
            try:
                self.repo.get_contents("backups", ref=self.branch)
            except:
                # Create backups directory if it doesn't exist
                self.repo.create_file(
                    "backups/.gitkeep",
                    "Create backups directory",
                    "",
                    branch=self.branch
                )
            
            # Create timestamp directory
            try:
                self.repo.get_contents(backup_prefix, ref=self.branch)
            except:
                pass
            
            # Backup each file
            for file_key, data in files_to_backup.items():
                backup_path = f"{backup_prefix}{self.DATA_FILES.get(file_key, file_key)}"
                content = json.dumps(data, indent=2, default=str)
                
                self.repo.create_file(
                    backup_path,
                    f"Backup: {file_key} data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    content,
                    branch=self.branch
                )
            
            return True
        except Exception as e:
            st.error(f"Error creating backup: {e}")
            return False
    
    def restore_from_backup(self, backup_timestamp, file_key="progress"):
        """Restore data from a specific backup"""
        if not self.repo:
            return None
        
        try:
            backup_path = f"backups/{backup_timestamp}/{self.DATA_FILES.get(file_key, file_key)}"
            contents = self.repo.get_contents(backup_path, ref=self.branch)
            content = base64.b64decode(contents.content).decode('utf-8')
            return json.loads(content)
        except:
            return None
    
    def list_backups(self):
        """List available backups"""
        if not self.repo:
            return []
        
        backups = []
        try:
            contents = self.repo.get_contents("backups", ref=self.branch)
            for content in contents:
                if content.type == "dir":
                    backups.append(content.name)
            return sorted(backups, reverse=True)
        except:
            return []
    
    def is_available(self):
        """Check if GitHub storage is available"""
        return self.repo is not None
    
    def get_sync_status(self):
        """Get sync status for all data files"""
        if not self.repo:
            return {"available": False}
        
        status = {"available": True, "files": {}}
        for file_key, file_name in self.DATA_FILES.items():
            try:
                file_path = self._get_full_path(file_key)
                contents = self.repo.get_contents(file_path, ref=self.branch)
                status["files"][file_key] = {
                    "name": file_name,
                    "sha": contents.sha[:8],
                    "size": contents.size,
                    "last_modified": contents.last_modified if hasattr(contents, 'last_modified') else "Unknown"
                }
            except:
                status["files"][file_key] = {"name": file_name, "exists": False}
        
        return status


class LocalStorage:
    """Fallback local storage when GitHub is not available"""
    
    DATA_FILES = GitHubStorage.DATA_FILES
    
    def save_data(self, data, file_key="progress"):
        """Save data to local file"""
        try:
            file_name = GitHubStorage.DATA_FILES.get(file_key, f"{file_key}.json")
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except Exception as e:
            st.error(f"Error saving locally: {e}")
            return False
    
    def load_data(self, file_key="progress"):
        """Load data from local file"""
        try:
            file_name = GitHubStorage.DATA_FILES.get(file_key, f"{file_key}.json")
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            return None
    
    def save_all_data(self, data_dict):
        """Save multiple data files locally"""
        success = True
        for file_key, data in data_dict.items():
            if not self.save_data(data, file_key):
                success = False
        return success
    
    def load_all_data(self):
        """Load all data files locally"""
        all_data = {}
        for file_key in self.DATA_FILES.keys():
            data = self.load_data(file_key)
            if data is not None:
                all_data[file_key] = data
        return all_data
    
    def is_available(self):
        """Local storage is always available"""
        return True


# Initialize storage (tries GitHub first, falls back to local)
@st.cache_resource
def get_storage():
    """Get the appropriate storage handler"""
    github_storage = GitHubStorage()
    if github_storage.is_available():
        return github_storage
    else:
        st.warning("⚠️ GitHub storage not available. Using local file storage.")
        return LocalStorage()


# Data management functions for the app
class DataManager:
    """Central data manager that handles all data operations with proper storage"""
    
    def __init__(self):
        self.storage = get_storage()
        self._data_cache = {}
    
    def _get_initial_data(self, file_key):
        """Get initial data structure for a file"""
        initial_data = {
            "progress": {},
            "assignments": {"assignments": [], "submissions": {}},
            "custom_tasks": {"date_specific_tasks": {}},
            "attendance": {}
        }
        return initial_data.get(file_key, {})
    
    def load_data(self, file_key):
        """Load data with caching"""
        if file_key in self._data_cache:
            return self._data_cache[file_key]
        
        data = self.storage.load_data(file_key)
        if data is None:
            data = self._get_initial_data(file_key)
            # Save initial data
            self.storage.save_data(data, file_key)
        
        self._data_cache[file_key] = data
        return data
    
    def save_data(self, data, file_key):
        """Save data and update cache"""
        success = self.storage.save_data(data, file_key)
        if success:
            self._data_cache[file_key] = data
        return success
    
    def load_all_data(self):
        """Load all data files"""
        all_data = self.storage.load_all_data()
        for file_key, data in all_data.items():
            self._data_cache[file_key] = data
        return all_data
    
    def save_all_data(self, data_dict):
        """Save all data files"""
        success = self.storage.save_all_data(data_dict)
        if success:
            for file_key, data in data_dict.items():
                self._data_cache[file_key] = data
        return success
    
    def backup_all(self):
        """Create a backup of all data"""
        all_data = self.load_all_data()
        return self.storage.backup_data(all_data)
    
    def clear_cache(self):
        """Clear the data cache"""
        self._data_cache = {}
    
    def sync_from_github(self):
        """Force sync from GitHub"""
        self.clear_cache()
        return self.load_all_data()


# Helper functions for specific data types
def get_progress_data():
    """Get progress data for coordinators"""
    manager = DataManager()
    return manager.load_data("progress")

def save_progress_data(data):
    """Save progress data"""
    manager = DataManager()
    return manager.save_data(data, "progress")

def get_assignments_data():
    """Get assignments data"""
    manager = DataManager()
    return manager.load_data("assignments")

def save_assignments_data(data):
    """Save assignments data"""
    manager = DataManager()
    return manager.save_data(data, "assignments")

def get_custom_tasks_data():
    """Get custom tasks data"""
    manager = DataManager()
    return manager.load_data("custom_tasks")

def save_custom_tasks_data(data):
    """Save custom tasks data"""
    manager = DataManager()
    return manager.save_data(data, "custom_tasks")

def get_attendance_data():
    """Get attendance data"""
    manager = DataManager()
    return manager.load_data("attendance")

def save_attendance_data(data):
    """Save attendance data"""
    manager = DataManager()
    return manager.save_data(data, "attendance")
