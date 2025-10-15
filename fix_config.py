"""Fix for pydantic_settings import in config.py"""
# This helper provides backward compatibility for pydantic settings

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    try:
        from pydantic import BaseSettings
    except ImportError:
        print("Installing pydantic-settings...")
        import subprocess
        subprocess.check_call(["pip", "install", "pydantic-settings"])
        from pydantic_settings import BaseSettings

print("✅ pydantic-settings is available")

