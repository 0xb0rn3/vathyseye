#!/usr/bin/env python3
print("""
⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣷⣄⠀⠀⠀⠀⣾⣷⠀⠀⠀⠀⣠⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⠿⠃⠀⠀⠀⠉⠉⠁⠀⠀⠐⠿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣶⣶⣶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣶⣿⣿⡿⣿⣿⣿⡿⠋⠉⠀⠀⠉⠙⢿⣿⣿⡿⣿⣿⣷⣦⡀⠀⠀⠀
⠀⢀⣼⣿⣿⠟⠁⢠⣿⣿⠏⠀⠀⢠⣤⣤⡀⠀⠀⢻⣿⣿⡀⠙⢿⣿⣿⣦⠀⠀
⣰⣿⣿⡟⠁⠀⠀⢸⣿⣿⠀⠀⠀⢿⣿⣿⡟⠀⠀⠈⣿⣿⡇⠀⠀⠙⣿⣿⣷⡄
⠈⠻⣿⣿⣦⣄⠀⠸⣿⣿⣆⠀⠀⠀⠉⠉⠀⠀⠀⣸⣿⣿⠃⢀⣤⣾⣿⣿⠟⠁
⠀⠀⠈⠻⣿⣿⣿⣶⣿⣿⣿⣦⣄⠀⠀⠀⢀⣠⣾⣿⣿⣿⣾⣿⣿⡿⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢰⣷⡦⠀⠀⠀⢀⣀⣀⠀⠀⠀⢴⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⠟⠁⠀⠀⠀⠘⣿⡇⠀⠀⠀⠀⠙⢷⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠻⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀

                  VathysEye
    Scripted by b0urn3 | For hackers and Linux command line lovers
 Instagram: onlybyhive Email: q4n0@proton.me Github: github.com/q4n0
        IF IT EXISTS I'LL FIND IT
""")

import os
import re
import json
import csv
import paramiko
import logging
import argparse
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from colorama import init, Fore, Style
import configparser

init(autoreset=True)  # Initialize colorama

# Setup logging
logging.basicConfig(filename='vathyseye.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('vathyseye.ini')

def search_local_files(directory, file_pattern, file_extensions, regex_pattern=None, max_size=None):
    matches = []
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for root, _, files in os.walk(directory):
            for filename in files:
                future = executor.submit(process_file, root, filename, file_pattern, file_extensions, regex_pattern, max_size)
                futures.append(future)
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Searching files"):
            result = future.result()
            if result:
                matches.extend(result)
    return matches

def process_file(root, filename, file_pattern, file_extensions, regex_pattern, max_size):
    if file_extensions and not any(filename.lower().endswith(ext.lower()) for ext in file_extensions):
        return None
    if not re.match(file_pattern, filename, re.IGNORECASE):
        return None
    
    file_path = os.path.join(root, filename)
    if max_size and os.path.getsize(file_path) > max_size:
        return None
    
    if regex_pattern:
        try:
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                if re.search(regex_pattern, content, re.IGNORECASE):
                    return [file_path]
        except Exception as e:
            logging.warning(f"Error reading {file_path}: {str(e)}")
    else:
        return [file_path]
    return None

# ... (other functions remain largely the same, with minor improvements)

def interactive_menu():
    print(Fore.CYAN + "\nVathysEye - The Advanced Deep Search Tool")
    print(Fore.WHITE + "1. Local Search")
    print("2. Permission Search")
    print("3. SSH Search")
    print("4. Exit")
    return input(Fore.GREEN + "Choose an option: " + Style.RESET_ALL)

def main():
    parser = argparse.ArgumentParser(description="VathysEye - Advanced Deep Search Tool")
    parser.add_argument("--mode", choices=['local', 'permission', 'ssh'], help="Search mode")
    parser.add_argument("--directory", help="Directory to search")
    parser.add_argument("--pattern", help="File name pattern (regex)")
    parser.add_argument("--extensions", help="File extensions (comma-separated)")
    args = parser.parse_args()

    if args.mode:
        # Non-interactive mode
        if args.mode == 'local':
            results = search_local_files(args.directory, args.pattern, args.extensions.split(',') if args.extensions else None)
        elif args.mode == 'permission':
            results = check_permissions(args.directory, args.pattern)  # Using pattern as perm_code here
        elif args.mode == 'ssh':
            print("SSH search not available in non-interactive mode for security reasons.")
            return
        save_results_prompt(results)
    else:
        while True:
            choice = interactive_menu()
            
            if choice == '1':
                directory = input("Enter the directory to search: ")
                pattern = input("Enter the file pattern (regex): ")
                extensions = input("Enter file extensions (comma-separated) or leave blank for all files: ")
                
                # Perform the local search
                results = search_local_files(directory, pattern, extensions.split(',') if extensions else None)
                
                # Display the results
                if results:
                    print(Fore.GREEN + "\nSearch complete. Found files:")
                    for file in results:
                        print(Fore.WHITE + file)
                else:
                    print(Fore.RED + "\nNo files found matching the criteria.")
                
                input(Fore.YELLOW + "\nPress Enter to return to the main menu...")
            
            elif choice == '2':
                # Permission Search functionality (to be implemented)
                pass
            
            elif choice == '3':
                # SSH Search functionality (to be implemented)
                pass
            
            elif choice == '4':
                print(Fore.YELLOW + "Exiting VathysEye. Goodbye!")
                break
            
            else:
                print(Fore.RED + "Invalid choice, please try again.")

if __name__ == '__main__':
    main()
