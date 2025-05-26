#!/usr/bin/env python3
"""
Laravel Documentation Updater

This module handles automatic fetching and updating of Laravel documentation
from the official GitHub repository.
"""

import sys
import logging
import argparse
import shutil
import tempfile
from pathlib import Path
from typing import Dict
import urllib.request
import urllib.error
import zipfile
import json
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("laravel-docs-updater")

# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
LARAVEL_DOCS_REPO = "laravel/docs"
DEFAULT_VERSION = "12.x"
USER_AGENT = "Laravel-Docs-MCP/0.1.0"

class DocsUpdater:
    """Handles downloading and updating Laravel documentation from GitHub."""
    
    def __init__(self, target_dir: Path, version: str = DEFAULT_VERSION):
        """
        Initialize the documentation updater.
        
        Args:
            target_dir: Directory where docs should be stored
            version: Laravel version branch to pull documentation from (e.g., "12.x")
        """
        self.target_dir = target_dir
        self.version = version
        self.github_api_url = GITHUB_API_URL
        self.repo = LARAVEL_DOCS_REPO
        
        # Create metadata directory if it doesn't exist
        self.metadata_dir = target_dir / ".metadata"
        self.metadata_dir.mkdir(exist_ok=True)
        self.metadata_file = self.metadata_dir / "sync_info.json"
    
    def get_latest_commit(self) -> Dict:
        """Get information about the latest commit on the specified branch."""
        logger.debug(f"Getting latest commit info for {self.repo} on branch {self.version}")
        
        url = f"{self.github_api_url}/repos/{self.repo}/branches/{self.version}"
        
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": USER_AGENT,
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode())
                return {
                    "sha": data["commit"]["sha"],
                    "date": data["commit"]["commit"]["committer"]["date"],
                    "message": data["commit"]["commit"]["message"],
                    "url": data["commit"]["html_url"]
                }
        except urllib.error.HTTPError as e:
            if e.code == 403 and "rate limit" in str(e.reason).lower():
                logger.error("GitHub API rate limit exceeded. Try again later.")
            elif e.code == 404:
                logger.error(f"Branch {self.version} not found in repository {self.repo}")
            else:
                logger.error(f"HTTP error {e.code}: {e.reason}")
            raise
        except Exception as e:
            logger.error(f"Error fetching latest commit info: {str(e)}")
            raise
    
    def read_local_metadata(self) -> Dict:
        """Read local metadata about the last sync."""
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error reading metadata file: {str(e)}")
            return {}
    
    def write_local_metadata(self, data: Dict) -> None:
        """Write local metadata about the current sync."""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing metadata file: {str(e)}")
    
    def download_documentation(self) -> Path:
        """
        Download the Laravel documentation as a zip file.
        
        Returns:
            Path to the downloaded and extracted documentation directory
        """
        logger.info(f"Downloading documentation for Laravel {self.version}")
        
        # GitHub archive URL for the specific branch
        archive_url = f"https://github.com/{self.repo}/archive/refs/heads/{self.version}.zip"
        
        try:
            # Create a temporary directory
            with tempfile.TemporaryDirectory(delete=False) as temp_dir:
                temp_path = Path(temp_dir)
                zip_path = temp_path / "laravel_docs.zip"
                
                # Download the zip file
                logger.debug(f"Downloading from {archive_url}")
                request = urllib.request.Request(
                    archive_url,
                    headers={"User-Agent": USER_AGENT}
                )
                
                with urllib.request.urlopen(request) as response, open(zip_path, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                
                # Extract the zip file
                logger.debug(f"Extracting archive to {temp_path}")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_path)
                
                # Find the extracted directory (should be named like "docs-12.x")
                extracted_dirs = [d for d in temp_path.iterdir() if d.is_dir() and (d.name.startswith(f"{self.repo.split('/')[-1]}-"))]
                
                if not extracted_dirs:
                    raise FileNotFoundError("Could not find extracted documentation directory")
                
                extracted_dir = extracted_dirs[0]
                logger.debug(f"Found extracted directory: {extracted_dir}")
                
                # Return the directory containing markdown files
                return extracted_dir
        except Exception as e:
            logger.error(f"Error downloading documentation: {str(e)}")
            raise
    
    def needs_update(self) -> bool:
        """Check if documentation needs to be updated based on remote commits."""
        try:
            # Get the latest commit info
            latest_commit = self.get_latest_commit()
            
            # Get local metadata
            local_meta = self.read_local_metadata()
            
            # Check if we already have the latest version
            if local_meta.get("version") == self.version and local_meta.get("commit_sha") == latest_commit["sha"]:
                logger.info("Documentation is already up to date.")
                return False
            
            # If we reach here, an update is needed
            return True
        except Exception as e:
            logger.error(f"Error checking for updates: {str(e)}")
            logger.info("Assuming update is needed due to error")
            return True
    
    def update(self, force: bool = False) -> bool:
        """
        Update the documentation if needed or if forced.
        
        Args:
            force: Force update even if already up to date
            
        Returns:
            True if update was performed, False otherwise
        """
        if not force and not self.needs_update():
            return False
        
        try:
            # Get the latest commit info for metadata
            latest_commit = self.get_latest_commit()
            
            # Download the documentation
            source_dir = self.download_documentation()
            
            # Clear the target directory (except .metadata)
            for item in self.target_dir.iterdir():
                if item.name != ".metadata":
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
            
            # Copy files to the target directory
            for item in source_dir.iterdir():
                if item.is_dir():
                    shutil.copytree(item, self.target_dir / item.name)
                else:
                    shutil.copy2(item, self.target_dir / item.name)
            
            # Update metadata
            metadata = {
                "version": self.version,
                "commit_sha": latest_commit["sha"],
                "commit_date": latest_commit["date"],
                "commit_message": latest_commit["message"],
                "commit_url": latest_commit["url"],
                "sync_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            self.write_local_metadata(metadata)

            shutil.rmtree(source_dir.parent)  # Remove the temporary directory
            logger.debug(f"Removed temporary directory: {source_dir.parent}")
            
            logger.info(f"Documentation updated successfully to {self.version} ({latest_commit['sha'][:7]})")
            return True
        except Exception as e:
            logger.error(f"Error updating documentation: {str(e)}")
            raise

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Laravel Documentation Updater"
    )
    parser.add_argument(
        "--target-dir", 
        type=str,
        default="./docs",
        help="Path to store documentation (default: ./docs)"
    )
    parser.add_argument(
        "--version",
        type=str,
        default=DEFAULT_VERSION,
        help=f"Laravel version branch to use (default: {DEFAULT_VERSION})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force update even if already up to date"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check if update is needed, don't perform update"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for the Laravel Docs Updater."""
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Create target directory if it doesn't exist
    target_dir = Path(args.target_dir).resolve()
    target_dir.mkdir(parents=True, exist_ok=True)
    
    updater = DocsUpdater(target_dir, args.version)
    
    try:
        if args.check_only:
            needs_update = updater.needs_update()
            print(f"Documentation {'needs' if needs_update else 'does not need'} updating.")
            return 0 if not needs_update else 1
        else:
            updated = updater.update(force=args.force)
            return 1 if updated else 0
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Operation failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())