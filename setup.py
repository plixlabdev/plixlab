"""
PlixLab setup configuration with post-install asset downloading.
"""

from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
import subprocess
import sys
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self._download_assets()

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self._download_assets()

def _download_assets():
    """Download third-party web assets."""
    try:
        # Get the path to the download script
        import plixlab
        script_path = os.path.join(os.path.dirname(plixlab.__file__), 'download_assets.py')
        subprocess.check_call([sys.executable, script_path])
        print("Successfully downloaded third-party web assets")
    except Exception as e:
        print(f"Warning: Could not download web assets: {e}")
        print("PlixLab will still work, but some features may be limited")

# Monkey patch the methods
PostInstallCommand._download_assets = staticmethod(_download_assets)
PostDevelopCommand._download_assets = staticmethod(_download_assets)

if __name__ == "__main__":
    setup(
        cmdclass={
            'install': PostInstallCommand,
            'develop': PostDevelopCommand,
        },
    )
