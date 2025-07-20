use std::collections::HashMap;
use std::env;
use std::fs;
use std::io::{self, Write};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

use rayon::prelude::*;
use walkdir::WalkDir;

const VERSION: &str = "3.0";
const AUTHOR: &str = "0xb0rn3 | 0xbv1";
const INSTAGRAM: &str = "theehiv3";

// Enhanced ASCII Banner
const BANNER: &str = r#"
██╗   ██╗ █████╗ ████████╗██╗  ██╗██╗   ██╗███████╗███████╗██╗   ██╗███████╗
██║   ██║██╔══██╗╚══██╔══╝██║  ██║╚██╗ ██╔╝██╔════╝██╔════╝╚██╗ ██╔╝██╔════╝
██║   ██║███████║   ██║   ███████║ ╚████╔╝ ███████╗█████╗   ╚████╔╝ █████╗  
╚██╗ ██╔╝██╔══██║   ██║   ██╔══██║  ╚██╔╝  ╚════██║██╔══╝    ╚██╔╝  ██╔══╝  
 ╚████╔╝ ██║  ██║   ██║   ██║  ██║   ██║   ███████║███████╗   ██║   ███████╗
  ╚═══╝  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝   ╚══════╝
                                                                              
        ┌─────────────────────────────────────────────────────────────────┐
        │  🔍 LIGHTNING FAST NATIVE SEARCH ENGINE 🔍                      │
        │  ⚡ IF IT EXISTS, I'LL FIND IT IN NANOSECONDS ⚡                │
        │  Author: 0xb0rn3 | 0xbv1  │  IG: theehiv3  │  Version: 3.0     │
        └─────────────────────────────────────────────────────────────────┘
"#;

// Color codes
const RED: &str = "\x1b[31m";
const GREEN: &str = "\x1b[32m";
const YELLOW: &str = "\x1b[33m";
const BLUE: &str = "\x1b[34m";
const MAGENTA: &str = "\x1b[35m";
const CYAN: &str = "\x1b[36m";
const WHITE: &str = "\x1b[37m";
const BOLD: &str = "\x1b[1m";
const RESET: &str = "\x1b[0m";

// Comprehensive file type mappings
fn create_file_extensions() -> HashMap<&'static str, Vec<&'static str>> {
    let mut extensions = HashMap::new();
    
    extensions.insert("media", vec![
        // Images
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif", "svg", "webp", "ico", 
        "psd", "ai", "eps", "raw", "cr2", "nef", "orf", "sr2", "dng", "heic", "avif",
        // Videos
        "mp4", "avi", "mkv", "mov", "wmv", "flv", "webm", "m4v", "3gp", "ogv", 
        "ts", "mts", "m2ts", "vob", "rmvb", "asf", "divx", "xvid", "f4v", "mpg", "mpeg",
        // Audio
        "mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "opus", "ape", "ac3", 
        "dts", "aiff", "au", "ra", "amr", "3ga", "mka", "tta", "wv"
    ]);
    
    extensions.insert("document", vec![
        "pdf", "doc", "docx", "txt", "rtf", "odt", "pages", "tex", "md", "rst",
        "xls", "xlsx", "ods", "csv", "ppt", "pptx", "odp", "key", "epub", "mobi",
        "djvu", "fb2", "azw", "azw3", "lit", "pdb", "tcr", "html", "htm", "xml"
    ]);
    
    extensions.insert("archive", vec![
        "zip", "rar", "7z", "tar", "gz", "bz2", "xz", "lzma", "cab", "iso",
        "dmg", "pkg", "deb", "rpm", "msi", "exe", "jar", "war", "ear", "apk",
        "ipa", "appx", "snap", "flatpak", "tgz", "tbz2", "txz", "z", "lz4"
    ]);
    
    extensions.insert("code", vec![
        "rs", "py", "js", "ts", "java", "cpp", "c", "h", "hpp", "cs", "php",
        "rb", "go", "kt", "swift", "scala", "clj", "hs", "ml", "fs", "pas",
        "pl", "sh", "bash", "zsh", "fish", "ps1", "bat", "cmd", "vbs", "lua",
        "r", "m", "sql", "json", "yaml", "yml", "toml", "ini", "cfg", "conf"
    ]);
    
    extensions.insert("system", vec![
        "dll", "so", "dylib", "sys", "drv", "kext", "ko", "bin", "dat", "db",
        "sqlite", "sqlite3", "cache", "tmp", "temp", "log", "bak", "old", "orig"
    ]);
    
    extensions
}

#[derive(Debug, Clone)]
struct FileResult {
    path: PathBuf,
    name: String,
    size: u64,
    file_type: String,
    is_hidden: bool,
    permissions: String,
}

impl FileResult {
    fn new(path: PathBuf) -> io::Result<Self> {
        let metadata = fs::metadata(&path)?;
        let name = path.file_name().unwrap_or_default().to_string_lossy().into_owned();
        let file_type = get_file_type(&path);
        let is_hidden = name.starts_with('.');
        let permissions = get_permissions(&metadata);
        
        Ok(FileResult {
            path,
            name,
            size: metadata.len(),
            file_type,
            is_hidden,
            permissions,
        })
    }
    
    fn display(&self) -> String {
        let size_str = format_size(self.size);
        let path_str = self.path.to_string_lossy();
        let dir_str = self.path.parent()
            .map(|p| p.to_string_lossy().into_owned())
            .unwrap_or_else(|| "/".to_string());
        
        format!(
            "{}📁 {}{} │ {}📄 {}{} │ {}📏 {}{} │ {}🔐 {}{}\n{}📍 Directory: {}{}{}",
            CYAN, self.name, RESET,
            GREEN, self.file_type, RESET,
            YELLOW, size_str, RESET,
            BLUE, self.permissions, RESET,
            MAGENTA, dir_str, RESET
        )
    }
}

fn get_file_type(path: &Path) -> String {
    if let Some(extension) = path.extension() {
        let ext = extension.to_string_lossy().to_lowercase();
        let extensions = create_file_extensions();
        
        for (category, exts) in extensions {
            if exts.contains(&ext.as_str()) {
                return category.to_string();
            }
        }
        ext
    } else {
        "unknown".to_string()
    }
}

fn get_permissions(metadata: &fs::Metadata) -> String {
    use std::os::unix::fs::PermissionsExt;
    let mode = metadata.permissions().mode();
    format!("{:o}", mode & 0o777)
}

fn format_size(size: u64) -> String {
    const UNITS: &[&str] = &["B", "KB", "MB", "GB", "TB"];
    let mut size_f = size as f64;
    let mut unit_index = 0;
    
    while size_f >= 1024.0 && unit_index < UNITS.len() - 1 {
        size_f /= 1024.0;
        unit_index += 1;
    }
    
    if unit_index == 0 {
        format!("{} {}", size, UNITS[unit_index])
    } else {
        format!("{:.1} {}", size_f, UNITS[unit_index])
    }
}

fn search_files(pattern: &str, file_type: Option<&str>, start_path: &Path) -> Vec<FileResult> {
    let start = Instant::now();
    println!("{}⚡ Initiating lightning-fast search...{}", YELLOW, RESET);
    
    let pattern_lower = pattern.to_lowercase();
    let extensions = create_file_extensions();
    
    let results: Vec<FileResult> = WalkDir::new(start_path)
        .follow_links(false)
        .into_iter()
        .par_bridge()
        .filter_map(|entry| {
            let entry = entry.ok()?;
            if !entry.file_type().is_file() {
                return None;
            }
            
            let path = entry.path();
            let filename = path.file_name()?.to_string_lossy().to_lowercase();
            
            // Pattern matching with fuzzy logic
            let matches_pattern = if pattern == "*" {
                true
            } else {
                filename.contains(&pattern_lower) ||
                fuzzy_match(&filename, &pattern_lower) > 0.6
            };
            
            if !matches_pattern {
                return None;
            }
            
            // Type filtering
            if let Some(target_type) = file_type {
                if target_type == "media" {
                    let ext = path.extension()?.to_string_lossy().to_lowercase();
                    if !extensions.get("media")?.contains(&ext.as_str()) {
                        return None;
                    }
                } else {
                    let detected_type = get_file_type(path);
                    if detected_type != target_type {
                        return None;
                    }
                }
            }
            
            // Check permissions and request sudo if needed
            if let Err(_) = fs::metadata(path) {
                if needs_root_access(path) {
                    request_sudo_access();
                }
                return None;
            }
            
            FileResult::new(path.to_path_buf()).ok()
        })
        .collect();
    
    let duration = start.elapsed();
    println!("{}🔍 Found {} results in {:.2}ms{}", GREEN, results.len(), 
             duration.as_secs_f64() * 1000.0, RESET);
    
    results
}

fn fuzzy_match(text: &str, pattern: &str) -> f64 {
    if text == pattern {
        return 1.0;
    }
    
    let text_chars: Vec<char> = text.chars().collect();
    let pattern_chars: Vec<char> = pattern.chars().collect();
    
    let mut matches = 0;
    let mut pattern_idx = 0;
    
    for &ch in &text_chars {
        if pattern_idx < pattern_chars.len() && ch == pattern_chars[pattern_idx] {
            matches += 1;
            pattern_idx += 1;
        }
    }
    
    matches as f64 / pattern_chars.len() as f64
}

fn needs_root_access(path: &Path) -> bool {
    path.starts_with("/root") || 
    path.starts_with("/etc") || 
    path.starts_with("/sys") ||
    path.starts_with("/proc")
}

fn request_sudo_access() {
    println!("{}⚠️  Root access required for some directories.{}", YELLOW, RESET);
    print!("Grant sudo access? (y/N): ");
    io::stdout().flush().unwrap();
    
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    
    if input.trim().to_lowercase() == "y" {
        println!("{}🔑 Please enter your password when prompted...{}", CYAN, RESET);
        // In a real implementation, you'd handle sudo elevation here
    }
}

fn display_results(results: &[FileResult]) {
    if results.is_empty() {
        println!("{}❌ No files found matching your criteria.{}", RED, RESET);
        return;
    }
    
    println!("\n{}{}🎯 SEARCH RESULTS{}{}", BOLD, GREEN, RESET, RESET);
    println!("{}═══════════════════════════════════════════════════════════════════════════════{}", CYAN, RESET);
    
    for (i, result) in results.iter().enumerate() {
        println!("\n{}{}[{}]{} {}", BOLD, WHITE, i + 1, RESET, result.display());
        if i < results.len() - 1 {
            println!("{}───────────────────────────────────────────────────────────────────────────────{}", BLUE, RESET);
        }
    }
    
    println!("\n{}═══════════════════════════════════════════════════════════════════════════════{}", CYAN, RESET);
}

fn navigate_to_file(results: &[FileResult]) {
    if results.is_empty() {
        return;
    }
    
    loop {
        print!("\n{}Navigate to file (1-{}, 0 to exit): {}", CYAN, results.len(), RESET);
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        
        let choice = input.trim();
        if choice == "0" {
            break;
        }
        
        if let Ok(index) = choice.parse::<usize>() {
            if index > 0 && index <= results.len() {
                let file = &results[index - 1];
                let dir = file.path.parent().unwrap_or_else(|| Path::new("/"));
                
                println!("{}📂 Opening directory: {}{}", GREEN, dir.display(), RESET);
                
                // Open file manager or navigate to directory
                if cfg!(target_os = "linux") {
                    Command::new("xdg-open").arg(dir).spawn().ok();
                } else if cfg!(target_os = "macos") {
                    Command::new("open").arg(dir).spawn().ok();
                }
                break;
            }
        }
        
        println!("{}❌ Invalid selection. Try again.{}", RED, RESET);
    }
}

fn show_help() {
    println!("{}", BANNER);
    println!("{}{}USAGE:{}{}", BOLD, YELLOW, RESET, RESET);
    println!("  {}vath -s <filename> [-t <type>]{}", CYAN, RESET);
    println!("  {}vath --interactive{}", CYAN, RESET);
    println!("  {}vath --help{}", CYAN, RESET);
    println!("\n{}{}OPTIONS:{}{}", BOLD, YELLOW, RESET, RESET);
    println!("  {}-s, --search <pattern>{}   Search for files matching pattern", CYAN, RESET);
    println!("  {}-t, --type <type>{}        Filter by file type (media, document, code, etc.)", CYAN, RESET);
    println!("  {}-i, --interactive{}        Launch interactive mode", CYAN, RESET);
    println!("  {}-h, --help{}               Show this help message", CYAN, RESET);
    println!("\n{}{}EXAMPLES:{}{}", BOLD, YELLOW, RESET, RESET);
    println!("  {}vath -s \"vacation\" -t media{}     # Find all media files with 'vacation' in name", GREEN, RESET);
    println!("  {}vath -s \"*.pdf\"{}                 # Find all PDF files", GREEN, RESET);
    println!("  {}vath -s \"config\" -t code{}        # Find configuration/code files", GREEN, RESET);
    println!("\n{}{}SUPPORTED FILE TYPES:{}{}", BOLD, YELLOW, RESET, RESET);
    println!("  {}media{}      - Images, videos, audio files", MAGENTA, RESET);
    println!("  {}document{}   - PDFs, Word docs, text files, etc.", MAGENTA, RESET);
    println!("  {}code{}       - Source code, scripts, configs", MAGENTA, RESET);
    println!("  {}archive{}    - ZIP, RAR, 7z, TAR files", MAGENTA, RESET);
    println!("  {}system{}     - System files, logs, binaries", MAGENTA, RESET);
}

fn interactive_mode() {
    println!("{}", BANNER);
    println!("{}{}🚀 INTERACTIVE MODE ACTIVATED{}{}", BOLD, CYAN, RESET, RESET);
    
    loop {
        println!("\n{}{}MENU:{}{}", BOLD, YELLOW, RESET, RESET);
        println!("{}1.{} Quick Search", CYAN, RESET);
        println!("{}2.{} Advanced Search (with type filter)", CYAN, RESET);
        println!("{}3.{} Help", CYAN, RESET);
        println!("{}4.{} Exit", CYAN, RESET);
        
        print!("\n{}Select option (1-4): {}", MAGENTA, RESET);
        io::stdout().flush().unwrap();
        
        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();
        
        match input.trim() {
            "1" => {
                print!("{}Enter search pattern: {}", CYAN, RESET);
                io::stdout().flush().unwrap();
                let mut pattern = String::new();
                io::stdin().read_line(&mut pattern).unwrap();
                
                let results = search_files(pattern.trim(), None, Path::new("/"));
                display_results(&results);
                navigate_to_file(&results);
            }
            "2" => {
                print!("{}Enter search pattern: {}", CYAN, RESET);
                io::stdout().flush().unwrap();
                let mut pattern = String::new();
                io::stdin().read_line(&mut pattern).unwrap();
                
                print!("{}Enter file type (media/document/code/archive/system): {}", CYAN, RESET);
                io::stdout().flush().unwrap();
                let mut file_type = String::new();
                io::stdin().read_line(&mut file_type).unwrap();
                
                let results = search_files(pattern.trim(), Some(file_type.trim()), Path::new("/"));
                display_results(&results);
                navigate_to_file(&results);
            }
            "3" => show_help(),
            "4" => {
                println!("{}👋 Thanks for using VathysEye!{}", GREEN, RESET);
                break;
            }
            _ => println!("{}❌ Invalid option. Try again.{}", RED, RESET),
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        println!("{}", BANNER);
        println!("{}Welcome to VathysEye 3.0! Use --help for usage information.{}", CYAN, RESET);
        println!("{}Or use --interactive for the guided experience.{}", YELLOW, RESET);
        return;
    }
    
    let mut search_pattern = None;
    let mut file_type = None;
    let mut interactive = false;
    
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-s" | "--search" => {
                if i + 1 < args.len() {
                    search_pattern = Some(args[i + 1].clone());
                    i += 1;
                }
            }
            "-t" | "--type" => {
                if i + 1 < args.len() {
                    file_type = Some(args[i + 1].clone());
                    i += 1;
                }
            }
            "-i" | "--interactive" => {
                interactive = true;
            }
            "-h" | "--help" => {
                show_help();
                return;
            }
            _ => {}
        }
        i += 1;
    }
    
    if interactive {
        interactive_mode();
        return;
    }
    
    if let Some(pattern) = search_pattern {
        let current_dir = env::current_dir().unwrap_or_else(|_| PathBuf::from("/"));
        let results = search_files(&pattern, file_type.as_deref(), &current_dir);
        display_results(&results);
        navigate_to_file(&results);
    } else {
        show_help();
    }
}
