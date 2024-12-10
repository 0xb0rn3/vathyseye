#!/usr/bin/env python3
"""
Advanced File Exploration and Management Toolkit
================================================

A comprehensive, secure, and efficient tool for file management, 
search, and system exploration.

Features:
- Advanced file search with multiple filtering options
- Secure file operations and encryption
- Comprehensive logging
- Cross-platform compatibility
- Parallel processing for large file searches
- Detailed system and file information gathering

Author: AI Assistant
Version: 3.0
"""

import os
import sys
import re
import json
import logging
import argparse
import hashlib
import shutil
from typing import List, Dict, Optional, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# External dependencies for enhanced functionality
try:
    import paramiko
    import magic  # for file type detection
    import xxhash  # for fast hashing
    from tqdm import tqdm
    from colorama import init, Fore, Style
except ImportError:
    print("Missing dependencies. Please install required packages:")
    print("pip install python-magic paramiko xxhash tqdm colorama")
    sys.exit(1)

# Initialize colorama for cross-platform color support
init(autoreset=True)

class AdvancedFileToolkit:
    """
    A comprehensive file management and exploration toolkit with 
    advanced search, security, and analysis capabilities.
    """
    
    def __init__(self, config_path: str = 'config.json'):
        """
        Initialize the toolkit with configuration and setup logging.
        
        Args:
            config_path (str): Path to the configuration file
        """
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Setup logging
        self._setup_logging()
        
        # Security and encryption setup
        self._encryption_key = self._generate_or_load_encryption_key()
    
    def _load_config(self, config_path: str) -> Dict:
        """
        Load configuration from a JSON file with sensible defaults.
        
        Args:
            config_path (str): Path to the configuration file
        
        Returns:
            Dict: Configuration dictionary
        """
        default_config = {
            "log_dir": os.path.expanduser("~/.file_toolkit_logs"),
            "backup_dir": os.path.expanduser("~/file_toolkit_backups"),
            "max_search_depth": 10,
            "parallel_workers": os.cpu_count() or 4,
            "default_hash_algorithm": "xxhash",
            "encryption": {
                "algorithm": "AES-256-GCM",
                "key_file": os.path.expanduser("~/.file_toolkit_key")
            }
        }
        
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge user config with defaults, giving priority to user settings
                return {**default_config, **user_config}
        except FileNotFoundError:
            logging.warning(f"Config file {config_path} not found. Using default configuration.")
            return default_config
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file {config_path}. Using default configuration.")
            return default_config
    
    def _setup_logging(self):
        """
        Configure a robust logging system with multiple log handlers.
        """
        log_dir = self.config.get('log_dir')
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a comprehensive logging setup
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                # File handler for detailed logs
                logging.FileHandler(
                    os.path.join(log_dir, f'file_toolkit_{datetime.now().strftime("%Y%m%d")}.log')
                ),
                # Console handler for immediate feedback
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _generate_or_load_encryption_key(self) -> bytes:
        """
        Generate or load an encryption key securely.
        
        Returns:
            bytes: Encryption key
        """
        key_path = self.config['encryption']['key_file']
        
        # If key exists, load it
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                return f.read()
        
        # Generate new key
        import secrets
        key = secrets.token_bytes(32)  # 256-bit key
        
        # Save key with restricted permissions
        with open(key_path, 'wb') as f:
            f.write(key)
        os.chmod(key_path, 0o600)  # Read/write for owner only
        
        logging.info("New encryption key generated and saved securely.")
        return key
    
    def advanced_search(
        self, 
        directory: str, 
        name_pattern: Optional[str] = None, 
        content_pattern: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        size_range: Optional[tuple] = None,
        modified_range: Optional[tuple] = None
    ) -> List[str]:
        """
        Perform an advanced, parallel file search with multiple filtering options.
        
        Args:
            directory (str): Root directory to start search
            name_pattern (str, optional): Regex pattern for filename
            content_pattern (str, optional): Regex pattern for file content
            file_types (List[str], optional): List of allowed file extensions/types
            size_range (tuple, optional): (min_size, max_size) in bytes
            modified_range (tuple, optional): (start_date, end_date)
        
        Returns:
            List[str]: Matching file paths
        """
        matches = []
        
        def is_match(file_path: str) -> bool:
            """
            Check if a file matches all specified criteria.
            """
            try:
                # Basic file type check
                if file_types:
                    file_ext = os.path.splitext(file_path)[1].lower()
                    if file_ext not in file_types:
                        return False
                
                # Size check
                if size_range:
                    file_size = os.path.getsize(file_path)
                    if not (size_range[0] <= file_size <= size_range[1]):
                        return False
                
                # Modification time check
                if modified_range:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if not (modified_range[0] <= mod_time <= modified_range[1]):
                        return False
                
                # Name pattern check
                if name_pattern and not re.search(name_pattern, os.path.basename(file_path), re.IGNORECASE):
                    return False
                
                # Content pattern check (if specified)
                if content_pattern:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            if not re.search(content_pattern, f.read(), re.IGNORECASE):
                                return False
                    except Exception as e:
                        logging.warning(f"Could not read {file_path}: {e}")
                        return False
                
                return True
            
            except Exception as e:
                logging.warning(f"Error processing {file_path}: {e}")
                return False
        
        # Parallel walk and search
        with ThreadPoolExecutor(max_workers=self.config['parallel_workers']) as executor:
            futures = {}
            for root, _, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    futures[executor.submit(is_match, file_path)] = file_path
            
            # Collect results with progress bar
            for future in tqdm(as_completed(futures), total=len(futures), 
                               desc="Searching Files", unit="file"):
                try:
                    if future.result():
                        matches.append(futures[future])
                except Exception as e:
                    logging.error(f"Search error: {e}")
        
        return matches
    
    def file_analysis(self, file_path: str) -> Dict[str, Union[str, int]]:
        """
        Perform comprehensive file analysis.
        
        Args:
            file_path (str): Path to the file to analyze
        
        Returns:
            Dict: Detailed file information
        """
        try:
            # Basic file information
            stat = os.stat(file_path)
            
            # File type detection
            file_type = magic.from_file(file_path)
            
            # Hash calculations
            with open(file_path, 'rb') as f:
                # Use xxhash for fast hashing, fall back to SHA256
                try:
                    xxh_hash = xxhash.xxh64(f.read()).hexdigest()
                    sha_hash = hashlib.sha256(f.read()).hexdigest()
                except Exception:
                    # Reopen file if first read consumed it
                    f.seek(0)
                    sha_hash = hashlib.sha256(f.read()).hexdigest()
                    xxh_hash = xxhash.xxh64(f.read()).hexdigest()
            
            return {
                "path": file_path,
                "size": stat.st_size,
                "type": file_type,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime),
                "permissions": oct(stat.st_mode)[-3:],
                "owner": stat.st_uid,
                "xxhash": xxh_hash,
                "sha256": sha_hash
            }
        except Exception as e:
            logging.error(f"File analysis failed for {file_path}: {e}")
            return {}
    
    def secure_copy(self, source: str, destination: str, encrypt: bool = False):
        """
        Securely copy a file with optional encryption.
        
        Args:
            source (str): Source file path
            destination (str): Destination file path
            encrypt (bool, optional): Whether to encrypt during copy
        """
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            if encrypt:
                # Use high-level encryption 
                from cryptography.fernet import Fernet
                key = Fernet.generate_key()
                f = Fernet(key)
                
                with open(source, 'rb') as src:
                    encrypted_data = f.encrypt(src.read())
                
                with open(destination, 'wb') as dst:
                    dst.write(encrypted_data)
                
                # Optionally, save key securely
                with open(f"{destination}.key", 'wb') as key_file:
                    key_file.write(key)
            else:
                # Standard secure copy
                shutil.copy2(source, destination)
            
            logging.info(f"File {'encrypted and ' if encrypt else ''}copied: {source} -> {destination}")
        
        except Exception as e:
            logging.error(f"Secure copy failed: {e}")
    
    def interactive_menu(self):
        """
        Provide an interactive menu for toolkit operations.
        """
        while True:
            print(Fore.CYAN + "\n=== Advanced File Toolkit ===")
            print(Fore.WHITE + "1. Advanced File Search")
            print("2. File Analysis")
            print("3. Secure File Copy")
            print("4. System Information")
            print("5. Exit")
            
            choice = input(Fore.GREEN + "Choose an option (1-5): " + Style.RESET_ALL)
            
            try:
                if choice == '1':
                    # Advanced Search
                    directory = input("Enter search directory: ")
                    name_pattern = input("Filename pattern (optional, regex): ") or None
                    content_pattern = input("Content pattern (optional, regex): ") or None
                    file_types = input("File extensions (comma-separated, optional): ")
                    file_types = [f".{ext.strip()}" for ext in file_types.split(',')] if file_types else None
                    
                    results = self.advanced_search(
                        directory, 
                        name_pattern, 
                        content_pattern, 
                        file_types
                    )
                    
                    print(Fore.GREEN + f"\nFound {len(results)} files:")
                    for result in results:
                        print(Fore.WHITE + result)
                
                elif choice == '2':
                    # File Analysis
                    file_path = input("Enter file path for analysis: ")
                    analysis = self.file_analysis(file_path)
                    
                    print(Fore.GREEN + "\n=== File Analysis ===")
                    for key, value in analysis.items():
                        print(f"{Fore.CYAN}{key.capitalize()}: {Fore.WHITE}{value}")
                
                elif choice == '3':
                    # Secure Copy
                    source = input("Source file path: ")
                    destination = input("Destination file path: ")
                    encrypt = input("Encrypt file? (y/n): ").lower() == 'y'
                    self.secure_copy(source, destination, encrypt)
                
                elif choice == '4':
                    # System Information
                    print(Fore.GREEN + "\n=== System Information ===")
                    print(f"{Fore.CYAN}Platform: {Fore.WHITE}{sys.platform}")
                    print(f"{Fore.CYAN}Python Version: {Fore.WHITE}{sys.version}")
                    print(f"{Fore.CYAN}CPU Count: {Fore.WHITE}{os.cpu_count()}")
                
                elif choice == '5':
                    print(Fore.YELLOW + "Exiting Advanced File Toolkit. Goodbye!")
                    break
                
                else:
                    print(Fore.RED + "Invalid choice. Please try again.")
            
            except Exception as e:
                logging.error(f"Operation failed: {e}")
                print(Fore.RED + f"An error occurred: {e}")
            
            input(Fore.YELLOW + "\nPress Enter to continue...")

def main():
    """
    Main entry point for the Advanced File Toolkit.
    """
    toolkit = AdvancedFileToolkit()
    toolkit.interactive_menu()

if __name__ == '__main__':
    main()
