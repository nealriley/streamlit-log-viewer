import streamlit as st
import os
import tempfile
import time
from streamlit_file_reader import file_reader_component, file_reader_with_path_selector

# Page configuration
st.set_page_config(
    page_title="File Reader Component Demo",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
st.sidebar.title("📁 File Reader Demo")
demo_mode = st.sidebar.selectbox(
    "Choose Demo Mode",
    [
        "Basic File Reader",
        "File Reader with Path Selector", 
        "Log File Monitor Demo",
        "Create Test Files"
    ]
)

st.title("🚀 Streamlit File Reader Component Demo")

if demo_mode == "Basic File Reader":
    st.header("Basic File Reader Component")
    st.write("This demo shows the basic file reading functionality.")
    
    # File path input
    default_file = "/etc/hosts"  # Common file on most systems
    file_path = st.text_input(
        "File path to read:",
        value=default_file,
        help="Enter the full path to a file you want to read"
    )
    
    if file_path:
        # Component settings
        col1, col2, col3 = st.columns(3)
        
        with col1:
            max_lines = st.number_input("Max lines", min_value=10, max_value=500, value=50)
        
        with col2:
            show_line_numbers = st.checkbox("Show line numbers", value=True)
        
        with col3:
            auto_refresh = st.checkbox("Auto-refresh", value=False)
            if auto_refresh:
                refresh_interval = st.slider("Refresh interval (s)", 1.0, 10.0, 3.0)
            else:
                refresh_interval = 3.0
        
        st.divider()
        
        # Use the component
        content = file_reader_component(
            file_path=file_path,
            max_lines=max_lines,
            auto_refresh=auto_refresh,
            refresh_interval=refresh_interval,
            show_line_numbers=show_line_numbers
        )
        
        if content:
            st.sidebar.success(f"✅ Successfully read {len(content)} lines")
        else:
            st.sidebar.warning("⚠️ No content read")

elif demo_mode == "File Reader with Path Selector":
    st.header("File Reader with Built-in Path Selector")
    st.write("This demo includes a file path selector interface.")
    
    # Use the component with path selector
    content = file_reader_with_path_selector(
        default_path="/etc/passwd",  # Another common file
        max_lines=100,
        auto_refresh=False,
        refresh_interval=2.0,
        show_line_numbers=True
    )
    
    if content:
        st.sidebar.success(f"✅ Read {len(content)} lines")
        
        # Show some statistics
        with st.sidebar.expander("📊 Content Statistics"):
            total_chars = sum(len(line) for line in content)
            avg_line_length = total_chars / len(content) if content else 0
            
            st.metric("Total characters", f"{total_chars:,}")
            st.metric("Average line length", f"{avg_line_length:.1f}")
            st.metric("Longest line", f"{max(len(line) for line in content) if content else 0}")

elif demo_mode == "Log File Monitor Demo":
    st.header("Log File Monitoring Demo")
    st.write("This demo simulates real-time log file monitoring.")
    
    # Create a temporary log file for demonstration
    if 'demo_log_file' not in st.session_state:
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        st.session_state.demo_log_file = temp_file.name
        temp_file.close()
        
        # Write initial content
        with open(st.session_state.demo_log_file, 'w') as f:
            f.write("Demo log file created at " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            f.write("This is a demonstration of log file monitoring.\n")
            f.write("New entries will be added automatically.\n")
    
    log_file_path = st.session_state.demo_log_file
    
    st.info(f"📝 Demo log file: `{log_file_path}`")
    
    # Controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Log Entry"):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f"[{timestamp}] Manual log entry added via demo interface\n"
            
            with open(log_file_path, 'a') as f:
                f.write(log_entry)
            
            st.success("Log entry added!")
    
    with col2:
        auto_add = st.checkbox("🤖 Auto-add entries", value=False)
    
    with col3:
        if st.button("🗑️ Clear Log File"):
            with open(log_file_path, 'w') as f:
                f.write("Log file cleared at " + time.strftime('%Y-%m-%d %H:%M:%S') + "\n")
            st.success("Log file cleared!")
    
    # Auto-add entries if enabled
    if auto_add:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Automatic log entry #{int(time.time()) % 1000}\n"
        
        with open(log_file_path, 'a') as f:
            f.write(log_entry)
    
    st.divider()
    
    # Monitor the log file
    content = file_reader_component(
        file_path=log_file_path,
        max_lines=20,
        auto_refresh=True,
        refresh_interval=2.0,
        show_line_numbers=True
    )
    
    # Cleanup info
    st.sidebar.warning("🧹 The demo log file will be automatically cleaned up when you restart the app.")

elif demo_mode == "Create Test Files":
    st.header("Create Test Files")
    st.write("Create sample files to test the file reader component.")
    
    # Test file options
    test_file_type = st.selectbox(
        "Choose test file type:",
        [
            "Simple Text File",
            "Log File with Timestamps", 
            "Large Text File",
            "JSON-like Content",
            "Code File"
        ]
    )
    
    file_name = st.text_input(
        "File name:",
        value=f"test_{test_file_type.lower().replace(' ', '_')}.txt"
    )
    
    if st.button("📝 Create Test File"):
        file_path = os.path.join(os.getcwd(), file_name)
        
        try:
            if test_file_type == "Simple Text File":
                content = """Hello, World!
This is a simple test file.
It contains multiple lines of text.
Line 4: Some content here
Line 5: More content
Line 6: Even more content
Final line: End of file"""
            
            elif test_file_type == "Log File with Timestamps":
                current_time = time.time()
                content = ""
                for i in range(10):
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time - (10-i)*60))
                    content += f"[{timestamp}] INFO: Application started\n"
                    content += f"[{timestamp}] DEBUG: Loading configuration\n"
                    content += f"[{timestamp}] INFO: Server listening on port 8080\n"
            
            elif test_file_type == "Large Text File":
                content = ""
                for i in range(200):
                    content += f"Line {i+1:03d}: This is line {i+1} of a large text file with some sample content.\n"
            
            elif test_file_type == "JSON-like Content":
                content = """{
  "application": "demo_app",
  "version": "1.0.0",
  "logs": [
    {"timestamp": "2024-01-01T10:00:00Z", "level": "INFO", "message": "Application started"},
    {"timestamp": "2024-01-01T10:00:01Z", "level": "DEBUG", "message": "Loading config"},
    {"timestamp": "2024-01-01T10:00:02Z", "level": "INFO", "message": "Ready to serve requests"}
  ],
  "config": {
    "debug": true,
    "port": 8080,
    "host": "localhost"
  }
}"""
            
            elif test_file_type == "Code File":
                content = '''#!/usr/bin/env python3
"""
Sample Python script for testing file reader
"""

import os
import sys
from datetime import datetime

def main():
    """Main function"""
    print("Hello from test script!")
    
    # Get current timestamp
    now = datetime.now()
    print(f"Current time: {now}")
    
    # List current directory
    files = os.listdir(".")
    print(f"Files in current directory: {len(files)}")
    
    for i, file in enumerate(files[:5]):
        print(f"  {i+1}. {file}")

if __name__ == "__main__":
    main()
'''
            
            # Write the file
            with open(file_path, 'w') as f:
                f.write(content)
            
            st.success(f"✅ Created test file: `{file_path}`")
            st.info("You can now use this file path in the other demo modes.")
            
            # Show file preview
            st.subheader("File Preview:")
            lines = content.split('\n')
            preview_lines = lines[:10]
            if len(lines) > 10:
                preview_lines.append("... (truncated)")
            
            st.code('\n'.join(preview_lines))
            
        except Exception as e:
            st.error(f"❌ Error creating file: {str(e)}")

# Footer
st.divider()
st.markdown("""
### 🔗 Component Features
- ✅ Read any text file
- ✅ Display with or without line numbers  
- ✅ Configurable line limits
- ✅ Auto-refresh functionality
- ✅ File modification detection
- ✅ Error handling for missing files
- ✅ Performance optimized for large files

### 🚀 Next Steps
Try the different demo modes to explore all features of the file reader component!
""")

# Development info in sidebar
with st.sidebar.expander("ℹ️ Development Info"):
    st.write("**Component Location:** `streamlit_file_reader/`")
    st.write("**Demo App:** `demo_app.py`")
    st.write("**Requirements:** `streamlit >= 1.28.0`")