"""
WSGI entry point for production deployment
"""
import os
import sys

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app import create_app
    app = create_app()
except Exception as e:
    print(f"Error creating app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    app.run()
