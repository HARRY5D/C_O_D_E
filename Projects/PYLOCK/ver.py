import sys
import platform

print(f"Python Version: {platform.python_version()}")
print(f"Python Implementation: {platform.python_implementation()}")
print(f"Python Location: {sys.executable}")
print(f"System Platform: {platform.system()} {platform.release()}")