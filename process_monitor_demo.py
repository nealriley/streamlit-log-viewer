import streamlit as st
import subprocess
import threading
import tempfile
import os
import time
from pathlib import Path
from typing import Optional
from streamlit_file_reader import file_reader_component

class ProcessManager:
    """Manages subprocess execution with file output redirection"""
    
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.output_file: Optional[str] = None
        self.is_running = False
        self.start_time: Optional[float] = None
        
    def start_process(self, command: str, shell: bool = True) -> tuple[bool, str]:
        """Start a subprocess with output redirected to file"""
        if self.is_running:
            return False, "Process already running"
            
        try:
            # Create temporary output file
            temp_file = tempfile.NamedTemporaryFile(
                mode='w', 
                delete=False, 
                suffix='.log',
                prefix='process_output_'
            )
            self.output_file = temp_file.name
            temp_file.close()
            
            # Start process with output redirected
            self.process = subprocess.Popen(
                command,
                shell=shell,
                stdout=open(self.output_file, 'w'),
                stderr=subprocess.STDOUT,  # Combine stderr with stdout
                universal_newlines=True,
                bufsize=1  # Line buffered
            )
            
            self.is_running = True
            self.start_time = time.time()
            
            # Start monitoring thread
            monitor_thread = threading.Thread(
                target=self._monitor_process,
                daemon=True
            )
            monitor_thread.start()
            
            return True, f"Process started with PID {self.process.pid}"
            
        except Exception as e:
            return False, f"Failed to start process: {str(e)}"
    
    def stop_process(self) -> tuple[bool, str]:
        """Stop the running process"""
        if not self.is_running or not self.process:
            return False, "No process running"
            
        try:
            self.process.terminate()
            
            # Wait for process to terminate with timeout
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                self.process.kill()
                self.process.wait()
            
            self.is_running = False
            return True, "Process stopped successfully"
            
        except Exception as e:
            return False, f"Error stopping process: {str(e)}"
    
    def _monitor_process(self):
        """Monitor process in background thread"""
        if self.process:
            self.process.wait()  # Wait for process to complete
            if self.is_running:  # Only update if we haven't manually stopped
                self.is_running = False
    
    def cleanup(self):
        """Clean up resources"""
        if self.is_running:
            self.stop_process()
            
        # Close stdout file handle if still open
        if self.process and self.process.stdout and not self.process.stdout.closed:
            self.process.stdout.close()
            
        # Clean up temporary file
        if self.output_file and os.path.exists(self.output_file):
            try:
                os.unlink(self.output_file)
            except OSError:
                pass  # File might be in use
    
    def get_status(self) -> dict:
        """Get current process status"""
        if not self.process:
            return {
                "status": "Not Started",
                "pid": None,
                "runtime": 0,
                "return_code": None
            }
        
        runtime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "status": "Running" if self.is_running else "Stopped",
            "pid": self.process.pid,
            "runtime": runtime,
            "return_code": self.process.returncode
        }

# Page configuration
st.set_page_config(
    page_title="Process Monitor Demo",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'process_manager' not in st.session_state:
    st.session_state.process_manager = ProcessManager()

# Header
st.title("⚙️ Process Monitor Demo")
st.write("Start a shell process and monitor its output in real-time using the file reader component.")

# Sidebar with process controls
with st.sidebar:
    st.header("🎛️ Process Controls")
    
    # Command input
    st.subheader("Command Configuration")
    
    # Predefined script options
    script_type = st.selectbox(
        "Choose a script type:",
        [
            "Custom Command",
            "Long-running Counter", 
            "System Monitoring",
            "File Operations",
            "Network Ping",
            "Log Generator"
        ]
    )
    
    # Set default commands based on selection
    default_commands = {
        "Long-running Counter": "for i in {1..100}; do echo \"Count: $i - $(date)\"; sleep 2; done",
        "System Monitoring": "while true; do echo \"[$(date)] CPU: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}') | Memory: $(free -m | awk 'NR==2{printf \"%.1f%%\", $3*100/$2}')\"; sleep 3; done",
        "File Operations": "for file in /etc/*; do echo \"Processing: $file - Size: $(du -h \"$file\" 2>/dev/null | cut -f1)\"; sleep 1; done | head -20",
        "Network Ping": "ping -c 20 google.com",
        "Log Generator": "for i in {1..50}; do echo \"[$(date '+%Y-%m-%d %H:%M:%S')] INFO: Application event #$i - Processing data batch\"; sleep 1; done",
        "Custom Command": ""
    }
    
    command = st.text_area(
        "Shell command:",
        value=default_commands.get(script_type, ""),
        height=100,
        help="Enter the shell command or script to execute"
    )
    
    # Process control buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start Process", disabled=st.session_state.process_manager.is_running):
            if command.strip():
                success, message = st.session_state.process_manager.start_process(command)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter a command")
    
    with col2:
        if st.button("⏹️ Stop Process", disabled=not st.session_state.process_manager.is_running):
            success, message = st.session_state.process_manager.stop_process()
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
    
    # Cleanup button
    if st.button("🧹 Cleanup", help="Clean up temporary files and stop process"):
        st.session_state.process_manager.cleanup()
        st.success("Cleanup completed")
    
    # Process status
    st.subheader("📊 Process Status")
    status = st.session_state.process_manager.get_status()
    
    st.metric("Status", status["status"])
    if status["pid"]:
        st.metric("PID", status["pid"])
    st.metric("Runtime", f"{status['runtime']:.1f}s")
    if status["return_code"] is not None:
        st.metric("Return Code", status["return_code"])

# Main content area
if st.session_state.process_manager.output_file:
    st.subheader("📄 Process Output")
    
    # File monitoring controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        max_lines = st.number_input("Max lines", min_value=10, max_value=200, value=50)
    
    with col2:
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        
    with col3:
        show_line_numbers = st.checkbox("Show line numbers", value=True)
    
    if auto_refresh:
        refresh_interval = st.slider("Refresh interval (s)", 1.0, 10.0, 2.0)
    else:
        refresh_interval = 2.0
    
    # Display file info
    output_file_path = st.session_state.process_manager.output_file
    st.info(f"📁 Output file: `{output_file_path}`")
    
    # Use the file reader component to monitor the output
    content = file_reader_component(
        file_path=output_file_path,
        max_lines=max_lines,
        auto_refresh=auto_refresh,
        refresh_interval=refresh_interval,
        show_line_numbers=show_line_numbers,
        height=500
    )
    
    # Additional information
    if content:
        with st.expander("📈 Output Statistics"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Lines Read", len(content))
            
            with col2:
                total_chars = sum(len(line) for line in content)
                st.metric("Total Characters", f"{total_chars:,}")
            
            with col3:
                avg_length = total_chars / len(content) if content else 0
                st.metric("Avg Line Length", f"{avg_length:.1f}")

else:
    st.info("👆 Start a process from the sidebar to begin monitoring its output")
    
    # Show example commands
    st.subheader("💡 Example Commands")
    
    examples = {
        "Simple Counter": "for i in {1..10}; do echo \"Line $i: $(date)\"; sleep 1; done",
        "System Info": "echo \"System: $(uname -a)\"; echo \"Date: $(date)\"; echo \"Uptime: $(uptime)\"",
        "Directory Listing": "find /etc -name '*.conf' -type f | head -10 | while read file; do echo \"Config: $file\"; done",
        "Random Data": "for i in {1..20}; do echo \"Random: $RANDOM - $(date '+%H:%M:%S')\"; sleep 0.5; done"
    }
    
    for name, cmd in examples.items():
        with st.expander(f"📋 {name}"):
            st.code(cmd, language="bash")

# Footer with tips
st.divider()
st.markdown("""
### 💡 Tips for Process Monitoring

- **Long-running processes**: Use commands with loops or continuous output
- **Real-time updates**: Enable auto-refresh to see output as it's generated  
- **Resource management**: Use the cleanup button to free resources
- **Error handling**: Both stdout and stderr are captured in the output file
- **Process control**: Stop long-running processes gracefully with the stop button

### 🔧 Technical Details

This demo combines:
- Subprocess management with output redirection
- Real-time file monitoring using the file reader component
- Thread-safe process lifecycle management
- Automatic cleanup of temporary resources
""")