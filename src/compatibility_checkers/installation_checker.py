# src/compatibility_checkers/installation_checker.py
import subprocess
import sys
import re
from .base import CompatibilityChecker
from ..parsers import parse_requirement

class InstallationCompatibilityChecker(CompatibilityChecker):
    def attempt_install(self, requirement):
        """Attempt to install the package and return success status and error message."""
        print(f"Attempting to install: {requirement}")  # Debug print
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "install", requirement, "--dry-run"], 
                                    capture_output=True, text=True, check=True)
            print(f"Successfully installed: {requirement}")  # Debug print
            return True, None
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.strip()
            print(f"Installation failed for {requirement}: {error_output}")  # Debug print
            
            if "No space left on device" in error_output:
                return True, "No space left on device"
            elif "No matching distribution found for" in error_output:
                return False, "No matching distribution found"
            elif "Could not find a version that satisfies the requirement" in error_output:
                return False, "No compatible version found"
            elif "HTTP error 404" in error_output:
                return False, "Package not found on PyPI"
            elif "Ignored the following versions that require a different python version:" in error_output:
                return False, "Python version incompatibility"
            else:
                return False, f"Installation failed: {error_output}"

    def check_compatibility(self, requirement):
        print(f"Checking installation compatibility for: {requirement}")  # Debug print
        name, version_spec = parse_requirement(requirement)
        if not name:
            print(f"Invalid requirement format: {requirement}")  # Debug print
            return requirement, "KEEP", "Invalid requirement format"

        success, error_msg = self.attempt_install(requirement)
        if success:
            if error_msg == "No space left on device":
                print(f"{requirement} is kept despite no space left on device")  # Debug print
                return requirement, "KEEP", "Package is kept despite no space left on device"
            else:
                print(f"{requirement} is installable with specified version")  # Debug print
                return requirement, "KEEP", "Package is installable with specified version"
        else:
            if error_msg in ["No matching distribution found", "No compatible version found", "Python version incompatibility"]:
                print(f"{error_msg} for {requirement}")  # Debug print
                return requirement, "COMMENT", f"{error_msg}"
            elif error_msg == "Package not found on PyPI":
                print(f"{requirement} not found on PyPI")  # Debug print
                return requirement, "COMMENT", "Package not found on PyPI"
            else:
                # Try installing without version specification
                success, error_msg = self.attempt_install(name)
                if success:
                    print(f"{name} is installable without version constraint")  # Debug print
                    return name, "LOOSEN", f"Specified version not installable, but package is installable without version constraint"
                else:
                    print(f"{requirement} is not installable: {error_msg}")  # Debug print
                    return requirement, "COMMENT", f"Package is not installable: {error_msg}"

    def extract_python_version(self, error_output):
        """Extract the Python version range from the error output."""
        version_ranges = re.findall(r'Requires-Python ([^;]+);', error_output)
        if version_ranges:
            return ', '.join(version_ranges)
        return None