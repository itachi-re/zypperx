# ZypperX

<div align="center">

![ZypperX Logo](https://img.shields.io/badge/ZypperX-2.0.0--alpha-blue?style=for-the-badge)
[![License](https://img.shields.io/badge/License-GPL--3.0-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge&logo=python)](https://python.org)
[![openSUSE](https://img.shields.io/badge/openSUSE-Ready-73ba25?style=for-the-badge&logo=opensuse)](https://opensuse.org)

**A blazingly fast parallel wrapper for zypper that accelerates repository refreshes and package downloads**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [How It Works](#-how-it-works) • [Contributing](#-contributing)

</div>

---

## 🚀 Features

- **⚡ Parallel Operations**: Execute repository refreshes and package downloads concurrently with configurable job limits
- **🔒 Safe Isolation**: Uses chroot environments to prevent conflicts between parallel zypper instances
- **📊 Beautiful UI**: Rich progress bars and formatted output powered by the Rich library
- **🎯 Smart Caching**: Detects already-cached packages and skips unnecessary downloads
- **🔄 Seamless Handoff**: Downloads in parallel, then hands off to native zypper for installation
- **💾 Memory Efficient**: Cleans up resources aggressively to minimize system impact
- **🛡️ Lock Management**: Respects zypper's lock file to prevent system corruption

## 📋 Requirements

- **OS**: openSUSE Tumbleweed, Leap, or any SUSE-based distribution
- **Python**: 3.8 or higher
- **Privileges**: Root access (sudo)
- **System Tools**: `zypper`, `mount`, `umount`, `chroot`, `findmnt`

### Python Dependencies

```bash
pip install rich
```

## 📦 Installation

### Method 1: Direct Download

```bash
# Clone the repository
git clone https://github.com/itachi-re/zypperx.git
cd zypperx

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x zypperx.py

# Optional: Install system-wide
sudo ln -s "$(pwd)/zypperx.py" /usr/local/bin/zypperx
```

### Method 2: Install with pip (Coming Soon)

```bash
pip install zypperx
```

## 🎯 Usage

### Basic Commands

#### Refresh Repositories
```bash
# Refresh all enabled repositories in parallel
sudo zypperx refresh

# Force refresh (equivalent to zypper ref -f)
sudo zypperx refresh --force

# Use 20 parallel jobs instead of default 10
sudo zypperx refresh -j 20
```

#### Distribution Upgrade
```bash
# Download packages for dist-upgrade in parallel
sudo zypperx dist-upgrade

# Download only (don't install)
sudo zypperx dup --download-only

# Skip confirmation prompts
sudo zypperx dup -y
```

#### Install Packages
```bash
# Install packages with parallel downloads
sudo zypperx install firefox vlc gimp

# Download only
sudo zypperx in package1 package2 --download-only

# Auto-confirm
sudo zypperx in neovim -y
```

#### Install New Recommends
```bash
# Install newly available recommended packages
sudo zypperx install-new-recommends

# Download only
sudo zypperx inr --download-only
```

### Command Aliases

- `refresh` → `ref`
- `dist-upgrade` → `dup`
- `install` → `in`
- `install-new-recommends` → `inr`

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-j, --jobs N` | Number of parallel jobs | 10 |
| `-y, --no-confirm` | Skip confirmation prompts | False |
| `-f, --force` | Force refresh of repositories | False |
| `-d, --download-only` | Download packages without installing | False |
| `--version` | Show version information | - |

## 🔧 How It Works

### The Parallel Magic

ZypperX achieves parallelization by creating isolated chroot environments for each concurrent operation:

```
1. Create temporary workspace
2. For each parallel job:
   ├─ Create isolated chroot environment
   ├─ Mount necessary filesystems (read-only root, /dev, /tmp, etc.)
   ├─ Execute zypper command in isolation
   └─ Clean up mounts
3. Hand off to native zypper for final installation
```

### Architecture Overview

```
┌─────────────────────────────────────────────┐
│           ZypperX Main Process              │
├─────────────────────────────────────────────┤
│  • Parse commands                           │
│  • Acquire system lock                      │
│  • Calculate transaction (dry-run)          │
│  • Create temporary workspace               │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│       Parallel Worker Pool (async)           │
├──────────────────────────────────────────────┤
│  Worker 1    Worker 2    ...    Worker N     │
│  ├─chroot    ├─chroot           ├─chroot     │
│  ├─mount     ├─mount            ├─mount      │
│  ├─zypper    ├─zypper           ├─zypper     │
│  └─cleanup   └─cleanup          └─cleanup    │
└──────────────┬───────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────┐
│    Native Zypper (for installation)          │
└──────────────────────────────────────────────┘
```

### Why Chroot?

Zypper uses a global lock file (`/run/zypp.pid`) to prevent concurrent operations. ZypperX bypasses this by:

1. **Creating isolated environments**: Each worker operates in its own chroot
2. **Read-only root**: The base system is mounted read-only to prevent conflicts
3. **Shared cache**: `/var/cache/zypp` is bind-mounted to share downloaded packages
4. **Clean handoff**: After parallel downloads, native zypper performs the installation

## 📊 Performance Comparison

### Real-world benchmarks (10 repositories, 150 packages)

| Operation | Standard Zypper | ZypperX (10 jobs) | Speedup |
|-----------|-----------------|-------------------|---------|
| Repository Refresh | ~45s | ~8s | **5.6x** |
| Package Download (500MB) | ~120s | ~25s | **4.8x** |
| Full `dup` (download) | ~180s | ~35s | **5.1x** |

*Results vary based on network speed, repository count, and system resources.*

## ⚠️ Limitations & Known Issues

- **Alpha Software**: This is experimental. Always keep backups.
- **Network Load**: Parallel downloads can saturate bandwidth and strain repository mirrors
- **Resource Usage**: Creates multiple chroot environments; ensure adequate disk space in `/tmp`
- **Refresh Only**: Only speeds up download phase; installation is still sequential
- **No Transaction Support**: Cannot parallelize dependency resolution

## 🐛 Troubleshooting

### "Zypper is currently locked"
Another zypper instance is running. Wait for it to complete or:
```bash
sudo rm /run/zypp.pid  # Use with caution
```

### "Missing system tools"
Install required dependencies:
```bash
sudo zypper install mount util-linux
```

### Mounts not cleaned up
If ZypperX crashes, manually clean up:
```bash
# Find orphaned mounts
mount | grep zypperx_

# Unmount them
sudo umount -l /tmp/zypperx_*
```

### Permission denied errors
Ensure you're running with root privileges:
```bash
sudo zypperx [command]
```

## 🗺️ Roadmap

- [ ] Configuration file support (`~/.config/zypperx/config.toml`)
- [ ] Better error recovery and retry logic
- [ ] Package verification in parallel
- [ ] Delta RPM support
- [ ] Integration with `zypper dup --allow-vendor-change`
- [ ] Bandwidth throttling per worker
- [ ] Systemd service for scheduled updates
- [ ] GUI frontend

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Setup

```bash
git clone https://github.com/itachi-re/zypperx.git
cd zypperx

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
black zypperx.py
pylint zypperx.py
```

### Areas Needing Help

- Unit and integration tests
- Security audit (especially around chroot operations)
- Performance optimization
- Documentation improvements
- Repository mirror load balancing

## 📄 License

Copyright (C) 2025 itachi_re <xanbenson99@gmail.com>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Inspired by**: [zypperoni](https://github.com/pavinjosdev/zypperoni) by Pavin Joseph
- **Built with**: [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- **For the community**: openSUSE users and contributors

## 📬 Contact

**itachi_re** - xanbenson99@gmail.com

Project Link: [https://github.com/itachi-re/zypperx](https://github.com/itachi-re/zypperx)

---

<div align="center">

**⭐ If ZypperX saves you time, consider giving it a star! ⭐**

Made with ❤️ for the openSUSE community

</div>
