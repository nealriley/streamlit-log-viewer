import streamlit as st
import os
from pathlib import Path
from typing import Optional, List
import time


def file_reader_component(
    file_path: str,
    max_lines: int = 100,
    auto_refresh: bool = False,
    refresh_interval: float = 2.0,
    show_line_numbers: bool = True,
    height: int = 400
) -> Optional[List[str]]:
    """
    A Streamlit component that reads and displays file content.
    
    Parameters:
    -----------
    file_path : str
        Path to the file to read
    max_lines : int, default=100
        Maximum number of lines to display (shows last N lines)
    auto_refresh : bool, default=False
        Whether to automatically refresh the file content
    refresh_interval : float, default=2.0
        Seconds between auto-refreshes (only when auto_refresh=True)
    show_line_numbers : bool, default=True
        Whether to show line numbers
    height : int, default=400
        Height of the display area in pixels
    
    Returns:
    --------
    Optional[List[str]]
        List of lines read from the file, or None if file doesn't exist
    """
    
    # Initialize session state for this component instance
    component_key = f"file_reader_{hash(file_path)}"
    
    if f"{component_key}_content" not in st.session_state:
        st.session_state[f"{component_key}_content"] = []
        st.session_state[f"{component_key}_last_modified"] = 0
        st.session_state[f"{component_key}_file_size"] = 0
        st.session_state[f"{component_key}_error"] = None
    
    # File path validation and display
    st.write(f"**File:** `{file_path}`")
    
    try:
        file_path_obj = Path(file_path)
        
        # Check if file exists
        if not file_path_obj.exists():
            st.error(f"File not found: {file_path}")
            st.session_state[f"{component_key}_error"] = "File not found"
            return None
        
        # Check if it's actually a file
        if not file_path_obj.is_file():
            st.error(f"Path is not a file: {file_path}")
            st.session_state[f"{component_key}_error"] = "Not a file"
            return None
        
        # Get file stats
        file_stat = file_path_obj.stat()
        current_modified = file_stat.st_mtime
        current_size = file_stat.st_size
        
        # Check if file has been modified
        should_read = (
            current_modified != st.session_state[f"{component_key}_last_modified"] or
            current_size != st.session_state[f"{component_key}_file_size"] or
            not st.session_state[f"{component_key}_content"]
        )
        
        if should_read:
            try:
                # Read file content
                with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
                    lines = file.readlines()
                
                # Keep only the last max_lines
                if len(lines) > max_lines:
                    lines = lines[-max_lines:]
                
                # Strip newlines but preserve empty lines
                lines = [line.rstrip('\n\r') for line in lines]
                
                # Update session state
                st.session_state[f"{component_key}_content"] = lines
                st.session_state[f"{component_key}_last_modified"] = current_modified
                st.session_state[f"{component_key}_file_size"] = current_size
                st.session_state[f"{component_key}_error"] = None
                
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                st.session_state[f"{component_key}_error"] = str(e)
                return None
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("File Size", f"{current_size:,} bytes")
        
        with col2:
            modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_modified))
            st.metric("Last Modified", modified_time)
        
        with col3:
            total_lines = len(st.session_state[f"{component_key}_content"])
            st.metric("Lines Displayed", f"{total_lines:,}")
        
        # Control buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Refresh", key=f"{component_key}_refresh"):
                # Force refresh by clearing the modified time
                st.session_state[f"{component_key}_last_modified"] = 0
                st.rerun()
        
        with col2:
            clear_content = st.button("🗑️ Clear Display", key=f"{component_key}_clear")
            if clear_content:
                st.session_state[f"{component_key}_content"] = []
                st.success("Display cleared")
        
        # Display content
        content = st.session_state[f"{component_key}_content"]
        
        if content:
            # Create container with specified height
            with st.container():
                st.write(f"**Content** (showing last {len(content)} lines):")
                
                # Display lines with or without line numbers
                if show_line_numbers:
                    display_text = ""
                    start_line_num = max(1, file_stat.st_size // 80 - len(content) + 1) if file_stat.st_size > 0 else 1
                    
                    for i, line in enumerate(content):
                        line_num = start_line_num + i
                        display_text += f"{line_num:4d} | {line}\n"
                    
                    st.code(display_text, language=None, line_numbers=False)
                else:
                    display_text = "\n".join(content)
                    st.code(display_text, language=None)
        else:
            st.info("No content to display")
        
        # Auto-refresh functionality
        if auto_refresh:
            st.info(f"🔄 Auto-refresh enabled (every {refresh_interval}s)")
            
            # Use a placeholder to show countdown
            countdown_placeholder = st.empty()
            
            # Countdown and refresh
            for i in range(int(refresh_interval), 0, -1):
                countdown_placeholder.text(f"Next refresh in {i} seconds...")
                time.sleep(1)
            
            countdown_placeholder.empty()
            st.rerun()
        
        return content
        
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.session_state[f"{component_key}_error"] = str(e)
        return None


def file_reader_with_path_selector(
    default_path: str = "/var/log",
    max_lines: int = 100,
    auto_refresh: bool = False,
    refresh_interval: float = 2.0,
    show_line_numbers: bool = True,
    height: int = 400
) -> Optional[List[str]]:
    """
    File reader component with built-in path selector.
    
    Parameters:
    -----------
    default_path : str, default="/var/log"
        Default directory or file path
    Other parameters same as file_reader_component
    
    Returns:
    --------
    Optional[List[str]]
        List of lines read from the selected file, or None if no file selected
    """
    
    st.subheader("📁 File Reader")
    
    # Path input
    file_path = st.text_input(
        "Enter file path:",
        value=default_path,
        help="Enter the full path to the file you want to read"
    )
    
    if not file_path:
        st.warning("Please enter a file path")
        return None
    
    # Settings in expander
    with st.expander("⚙️ Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            max_lines = st.number_input(
                "Max lines to display",
                min_value=10,
                max_value=1000,
                value=max_lines,
                step=10
            )
            
            show_line_numbers = st.checkbox(
                "Show line numbers",
                value=show_line_numbers
            )
        
        with col2:
            auto_refresh = st.checkbox(
                "Auto-refresh",
                value=auto_refresh,
                help="Automatically refresh file content"
            )
            
            if auto_refresh:
                refresh_interval = st.slider(
                    "Refresh interval (seconds)",
                    min_value=1.0,
                    max_value=30.0,
                    value=refresh_interval,
                    step=0.5
                )
    
    # Use the main component
    return file_reader_component(
        file_path=file_path,
        max_lines=max_lines,
        auto_refresh=auto_refresh,
        refresh_interval=refresh_interval,
        show_line_numbers=show_line_numbers,
        height=height
    )