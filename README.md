# Streamlit File Reader Component

A powerful Streamlit component for reading, monitoring, and displaying file content in real-time. Perfect for log monitoring, file analysis, and real-time data streaming applications.

## ✨ Features

- 📁 **File Reading**: Read any text file with configurable line limits
- 🔄 **Auto-Refresh**: Real-time monitoring with configurable refresh intervals
- 📊 **Line Numbers**: Optional line number display
- 🎯 **Smart Detection**: Automatic file modification detection
- 🛡️ **Error Handling**: Robust error handling for missing or inaccessible files
- ⚡ **Performance**: Optimized for large files with efficient memory usage
- 🎨 **User-Friendly**: Clean, intuitive interface with file statistics

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**
```bash
git clone <your-repo-url>
cd streamlit-file-reader
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

Or install in development mode:
```bash
pip install -e .
```

### Running the Demo

Launch the interactive demo application:

```bash
streamlit run demo_app.py
```

This will open your browser to `http://localhost:8501` where you can:
- Test basic file reading functionality
- Try the path selector interface
- Monitor log files in real-time
- Create test files for experimentation

## 📖 Usage

### Basic Usage

```python
import streamlit as st
from streamlit_file_reader import file_reader_component

# Simple file reading
content = file_reader_component(
    file_path="/path/to/your/file.txt",
    max_lines=100,
    show_line_numbers=True
)

if content:
    st.write(f"Read {len(content)} lines from file")
```

### Real-time Log Monitoring

```python
from streamlit_file_reader import file_reader_component

# Monitor a log file with auto-refresh
content = file_reader_component(
    file_path="/var/log/application.log",
    max_lines=50,
    auto_refresh=True,
    refresh_interval=2.0,
    show_line_numbers=True
)
```

### Interactive File Selection

```python
from streamlit_file_reader import file_reader_with_path_selector

# Component with built-in file path input
content = file_reader_with_path_selector(
    default_path="/var/log",
    max_lines=100,
    auto_refresh=False
)
```

## 🔧 API Reference

### `file_reader_component()`

Main component for reading file content.

**Parameters:**
- `file_path` (str): Path to the file to read
- `max_lines` (int, default=100): Maximum number of lines to display (shows last N lines)
- `auto_refresh` (bool, default=False): Whether to automatically refresh the file content
- `refresh_interval` (float, default=2.0): Seconds between auto-refreshes
- `show_line_numbers` (bool, default=True): Whether to show line numbers
- `height` (int, default=400): Height of the display area in pixels

**Returns:**
- `Optional[List[str]]`: List of lines read from the file, or None if file doesn't exist

### `file_reader_with_path_selector()`

Component with built-in file path selector interface.

**Parameters:**
- `default_path` (str, default="/var/log"): Default directory or file path
- All other parameters same as `file_reader_component()`

**Returns:**
- `Optional[List[str]]`: List of lines read from the selected file

## 🎯 Use Cases

### 1. Log File Monitoring
Monitor application logs in real-time:
```python
# Monitor application logs
file_reader_component(
    file_path="/var/log/myapp/application.log",
    auto_refresh=True,
    refresh_interval=1.0,
    max_lines=30
)
```

### 2. Configuration File Viewing
Display configuration files:
```python
# View config files
file_reader_component(
    file_path="/etc/myapp/config.yaml",
    auto_refresh=False,
    show_line_numbers=True
)
```

### 3. Data File Analysis
Analyze data files:
```python
# Analyze CSV or data files
file_reader_component(
    file_path="/data/sample.csv",
    max_lines=200,
    show_line_numbers=True
)
```

## 🛠️ Development

### Project Structure
```
streamlit-file-reader/
├── streamlit_file_reader/      # Main component package
│   ├── __init__.py
│   └── file_reader.py         # Core component implementation
├── demo_app.py                # Interactive demo application
├── setup.py                  # Package setup
├── requirements.txt           # Dependencies
├── README.md                 # This file
└── .gitignore               # Git ignore patterns
```

### Development Setup

1. **Clone the repository**
```bash
git clone <repo-url>
cd streamlit-file-reader
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install in development mode**
```bash
pip install -e .
pip install -r requirements.txt
```

4. **Run the demo**
```bash
streamlit run demo_app.py
```

### Testing the Component

The demo application includes several test modes:

1. **Basic File Reader**: Test core functionality
2. **Path Selector**: Test the interactive file selection
3. **Log Monitor Demo**: Test real-time monitoring with a demo log file
4. **Create Test Files**: Generate sample files for testing

### Adding Features

The component is designed to be easily extensible. Key areas for enhancement:

- **File Format Support**: Add syntax highlighting for different file types
- **Search Functionality**: Add text search within file content
- **Export Options**: Add options to export or download file content
- **Filtering**: Add line filtering based on patterns or keywords
- **Performance**: Further optimize for very large files

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.0+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Known Issues

- Auto-refresh may cause high CPU usage with very frequent refresh intervals
- Very large files (>1GB) may cause memory issues
- File encoding is automatically detected but may not work for all file types

## 🔮 Roadmap

- [ ] Add syntax highlighting for code files
- [ ] Implement file search functionality
- [ ] Add support for binary file detection
- [ ] Create advanced filtering options
- [ ] Add export/download capabilities
- [ ] Support for remote file URLs
- [ ] Integration with cloud storage services

## 📞 Support

If you encounter any issues or have questions:

1. Check the demo application for examples
2. Review the API documentation above
3. Create an issue in the repository
4. Check existing issues for solutions

---

Happy file reading! 🎉