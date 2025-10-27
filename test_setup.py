#!/usr/bin/env python3
"""Test script to verify the dbt MCP setup."""

import os
import sys

def test_setup():
    """Test the dbt MCP setup."""
    print("🔧 Testing dbt MCP Setup")
    print("=" * 50)
    
    # Check if transforms directory exists
    transforms_dir = os.path.join(os.getcwd(), "transforms")
    if os.path.exists(transforms_dir):
        print("✅ Transforms directory exists:", transforms_dir)
    else:
        print("❌ Transforms directory not found:", transforms_dir)
        return False
    
    # Check if profiles.yml exists
    profiles_path = os.path.join(transforms_dir, "profiles", "profiles.yml")
    if os.path.exists(profiles_path):
        print("✅ profiles.yml exists:", profiles_path)
    else:
        print("❌ profiles.yml not found:", profiles_path)
        return False
    
    # Check if config.env exists
    config_path = os.path.join(os.getcwd(), "config.env")
    if os.path.exists(config_path):
        print("✅ config.env exists:", config_path)
    else:
        print("❌ config.env not found:", config_path)
        return False
    
    # Check if streamlit_app.py exists
    app_path = os.path.join(os.getcwd(), "streamlit_app.py")
    if os.path.exists(app_path):
        print("✅ streamlit_app.py exists:", app_path)
    else:
        print("❌ streamlit_app.py not found:", app_path)
        return False
    
    print("\n🚀 Setup Instructions:")
    print("1. Set your OpenAI API key in config.env")
    print("2. Run: uv run streamlit run streamlit_app.py")
    print("3. Open http://localhost:8501 in your browser")
    print("4. Start chatting with your dbt project!")
    
    return True

if __name__ == "__main__":
    test_setup()
