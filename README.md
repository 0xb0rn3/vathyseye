# VathysEye 👁️

## Overview

VathysEye is an advanced file search and indexing system designed to help you quickly locate and categorize files across your system. With powerful search capabilities, intelligent file categorization, and a user-friendly interface, VathysEye makes file management and discovery effortless.

```
⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⣷⣄⠀⠀⠀⠀⣾⣷⠀⠀⠀⠀⣠⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢿⠿⠃⠀⠀⠀⠉⠉⠁⠀⠀⠐⠿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣤⣶⣶⣶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣠⣶⣿⣿⡿⣿⣿⣿⡿⠋⠉⠀⠀⠉⠙⢿⣿⣿⡿⣿⣿⣷⣦⡀⠀⠀⠀
⠀⢀⣼⣿⣿⠟⠁⢠⣿⣿⠏⠀⠀⢠⣤⣤⡀⠀⠀⢻⣿⣿⡀⠙⢿⣿⣿⣦⠀⠀
⣰⣿⣿⡟⠁⠀⠀⢸⣿⣿⠀⠀⠀⢿⣿⣿⡟⠀⠀⠈⣿⣿⡇⠀⠀⠙⣿⣿⣷⡄
⠈⠻⣿⣿⣦⣄⠀⠸⣿⣿⣆⠀⠀⠀⠉⠉⠀⠀⠀⣸⣿⣿⠃⢀⣤⣾⣿⣿⠟⠁
                  VathysEye
        IF IT EXISTS I'LL FIND IT
```

## Features

- 🔍 **Advanced File Search**: Quickly find files using flexible search patterns
- 📂 **Intelligent File Categorization**: Automatically categorize files into types like video, image, document, archive, and more
- 💾 **SQLite Database Indexing**: Efficient file metadata tracking with comprehensive indexing
- 🌐 **Cross-Platform Support**: Works on multiple Linux distributions (apt, dnf, yum, pacman)
- 🔄 **Auto-Update Mechanism**: One-click updates directly from GitHub
- 🖥️ **Interactive Search Mode**: User-friendly interface for file discovery

## Requirements

- Bash
- SQLite3
- `file` utility
- `find`
- `grep`
- `curl`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/0xb0rn3/vathyseye.git
   cd vathyseye
   ```

2. Make the script executable:
   ```bash
   chmod +x run
   ```

## Usage

### Basic Commands

- **Interactive Search**: 
  ```bash
  ./run interactive
  ```

- **Search Files**: 
  ```bash
  ./run search [pattern]
  ```

- **Full System Indexing**:
  ```bash
  ./run index
  ```

- **Update VathysEye**:
  ```bash
  ./run update
  ```

## How It Works

VathysEye uses a sophisticated approach to file indexing and searching:

1. **Dependency Check**: Automatically checks and installs required tools
2. **Database Initialization**: Creates a SQLite database for efficient file tracking
3. **Intelligent Categorization**: Uses MIME types to classify files
4. **Flexible Search**: Supports regex-based searching with optional depth and category filters

## Configuration

- **Configuration Directory**: `~/.config/vathyseye`
- **Cache Directory**: `~/.cache/vathyseye`
- **Database Path**: `~/.cache/vathyseye/vathyseye.db`
- **Log File**: `~/.cache/vathyseye/vathyseye.log`

## Logging

VathysEye provides comprehensive logging with color-coded output:
- 🔴 ERROR: Critical issues
- 🟡 WARN: Potential problems
- 🟢 INFO: General information
- 🔵 DEBUG: Detailed diagnostic information

## Version

Current Version: 2.5
Author: 0xb0rn3

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Disclaimer

VathysEye is provided as-is. Always ensure you have proper permissions when searching and indexing files.
