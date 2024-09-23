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
#!/usr/bin/env python3
import os
import re
import json
import csv
import paramiko
import logging
from getpass import getpass
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def search_local_files(directory, file_pattern, file_extensions, regex_pattern=None, max_size=None):
    matches = []
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                if file_extensions:
                    if not any(filename.lower().endswith(ext.lower()) for ext in file_extensions):
                        continue
                if re.match(file_pattern, filename, re.IGNORECASE):
                    file_path = os.path.join(root, filename)
                    if max_size and os.path.getsize(file_path) > max_size:
                        continue
                    if regex_pattern:
                        try:
                            with open(file_path, 'r', errors='ignore') as f:
                                content = f.read()
                                if re.search(regex_pattern, content, re.IGNORECASE):
                                    matches.append(file_path)
                        except Exception as e:
                            logging.warning(f"Error reading {file_path}: {str(e)}")
                    else:
                        matches.append(file_path)
    except Exception as e:
        logging.error(f"Error searching {directory}: {str(e)}")
    return matches

def check_permissions(directory, perm_code):
    matches = []
    try:
        for root, _, files in os.walk(directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                try:
                    file_stat = os.stat(file_path)
                    if oct(file_stat.st_mode)[-3:] == perm_code:
                        matches.append(file_path)
                except Exception as e:
                    logging.warning(f"Error checking permissions for {file_path}: {str(e)}")
    except Exception as e:
        logging.error(f"Error walking directory {directory}: {str(e)}")
    return matches

def ssh_search_files(host, username, password, directory, file_pattern, file_extensions):
    matches = []
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)

        sftp = client.open_sftp()
        sftp.chdir(directory)

        for filename in sftp.listdir():
            if file_extensions:
                if not any(filename.lower().endswith(ext.lower()) for ext in file_extensions):
                    continue
            if re.match(file_pattern, filename, re.IGNORECASE):
                matches.append(f"{host}:{os.path.join(directory, filename)}")

        sftp.close()
        client.close()
    except Exception as e:
        logging.error(f"Error in SSH search for {host}: {str(e)}")
    return matches

def format_path(path):
    directory, filename = os.path.split(path)
    return f"Directory: {directory}\nFile: {filename}"

def format_results(results):
    formatted = "Search Results:\n" + "=" * 80 + "\n"
    for index, result in enumerate(results, start=1):
        formatted += f"Result {index}:\n"
        formatted += format_path(result) + "\n"
        formatted += "-" * 80 + "\n"
    formatted += f"Total results found: {len(results)}\n"
    formatted += "=" * 80 + "\n"
    return formatted

def print_results(results):
    if not results:
        print("No results found.")
        return
    print(format_results(results))

def save_results(file_format, results, output_file):
    try:
        formatted_results = format_results(results)
        if file_format == 'json':
            with open(output_file, 'w') as json_file:
                json.dump({
                    "formatted_output": formatted_results,
                    "raw_results": [{"directory": os.path.dirname(r), "filename": os.path.basename(r)} for r in results]
                }, json_file, indent=4)
        elif file_format == 'csv':
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['Index', 'Directory', 'Filename'])
                for index, result in enumerate(results, start=1):
                    writer.writerow([index, os.path.dirname(result), os.path.basename(result)])
        else:  # txt format
            with open(output_file, 'w') as txt_file:
                txt_file.write(formatted_results)
        logging.info(f"Results saved to {output_file}")
        print(f"Results have been saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving results to {output_file}: {str(e)}")

def save_results_prompt(results):
    if not results:
        print("No results found.")
        return
    
    print_results(results)  # Always print results
    
    save_choice = input("Do you want to save the results to a file? (yes/no): ").strip().lower()
    if save_choice == 'yes':
        save_format = input("Save results as (json/csv/txt): ").strip().lower()
        output_file = input("Enter the output file name: ")
        save_results(save_format, results, output_file)

def get_file_extensions():
    extensions = input("Enter file extensions to search for (comma-separated, leave empty for all): ").strip()
    return [ext.strip() for ext in extensions.split(',')] if extensions else []

def interactive_menu():
    print("\nVathysEye - The Advanced Deep Search Tool")
    print("1. Local Search")
    print("2. Permission Search")
    print("3. SSH Search")
    print("4. Exit")
    choice = input("Choose an option: ")
    return choice

def main():
    while True:
        choice = interactive_menu()
        
        if choice == '1':
            directory = input("Enter the directory to search: ")
            file_pattern = input("Enter the file name pattern (regex): ")
            file_extensions = get_file_extensions()
            regex_pattern = input("Enter the content pattern to search within files (regex, optional): ") or None
            max_size = input("Enter the maximum file size to consider (bytes, optional): ") or None
            results = search_local_files(directory, file_pattern, file_extensions, regex_pattern, int(max_size) if max_size else None)
            save_results_prompt(results)
        
        elif choice == '2':
            directory = input("Enter the directory to search: ")
            perm_code = input("Enter the permission code (e.g., 755): ")
            results = check_permissions(directory, perm_code)
            save_results_prompt(results)

        elif choice == '3':
            host = input("Enter the SSH host: ")
            username = input("Enter the SSH username: ")
            password = getpass("Enter the SSH password: ")
            directory = input("Enter the directory to search: ")
            file_pattern = input("Enter the file name pattern (regex): ")
            file_extensions = get_file_extensions()
            results = ssh_search_files(host, username, password, directory, file_pattern, file_extensions)
            save_results_prompt(results)
        
        elif choice == '4':
            print("Exiting VathysEye. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()