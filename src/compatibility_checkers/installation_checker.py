import subprocess
import sys
import re
from .base import CompatibilityChecker
from ..parsers import parse_requirement

class InstallationCompatibilityChecker(CompatibilityChecker):
    """
    A class for checking the installation compatibility of Python packages and handling installation attempts.

    This class attempts to install Python packages, handles errors related to installation, and retries installation
    with loosened version constraints if necessary. It also extracts specific Python version requirements from errors.
    """



    def attempt_install(self, requirement):
        """
        Attempt to install a given package and return the success status along with any error messages.
        
        The installation is run in dry-run mode (`--dry-run`) to avoid actual package installation, simulating the process 
        to check whether it would succeed or fail. This helps in determining compatibility issues.

        Args:
            requirement (str): The package requirement (including version constraints) to attempt installing.

        Returns:
            tuple: A tuple containing:
                - (bool) True if installation succeeds, False otherwise.
                - (str) Error message if the installation fails, or None if successful.
        """
        print(f"Attempting to install: {requirement}")  # Debug print
        try:
            # Use pip with --dry-run to simulate the installation without actually installing the package
            result = subprocess.run([sys.executable, "-m", "pip", "install", requirement, "--dry-run"], 
                                    capture_output=True, text=True, check=True)
            print(f"Successfully installed: {requirement}")  # Debug print
            return True, None
        except subprocess.CalledProcessError as e:
            error_output = e.stderr.strip()
            print(f"Installation failed for {requirement}: {error_output}")  # Debug print

            # Handle specific error messages
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
        """
        Check the installation compatibility of a given package requirement and determine appropriate actions.

        This method parses the requirement, attempts to install the package, and returns appropriate actions
        based on whether the installation was successful or failed. If the installation fails due to version
        incompatibility, it loosens the version constraints and retries the installation.

        Args:
            requirement (str): The package requirement string (e.g., `package_name==1.0.0`).

        Returns:
            tuple: A tuple containing:
                - (str) The requirement name or modified version if constraints were loosened.
                - (str) The action to take, either 'KEEP', 'LOOSEN', or 'COMMENT'.
                - (str) A message explaining the reason for the action taken.
        """
        print(f"Checking installation compatibility for: {requirement}")  # Debug print
        name, version_spec = parse_requirement(requirement)
        
        # If the requirement format is invalid, return an error message
        if not name:
            print(f"Invalid requirement format: {requirement}")  # Debug print
            return requirement, "KEEP", "Invalid requirement format"

        # Attempt to install the package with the specified version
        success, error_msg = self.attempt_install(requirement)
        if success:
            # Special case for "No space left on device" error
            if error_msg == "No space left on device":
                print(f"{requirement} is kept despite no space left on device")  # Debug print
                return requirement, "KEEP", "Package is kept despite no space left on device"
            else:
                # Installation successful with the specified version
                print(f"{requirement} is installable with specified version")  # Debug print
                return requirement, "KEEP", "Package is installable with specified version"
        else:
            # Handle specific errors
            if error_msg in ["No matching distribution found", "No compatible version found"]:
                print(f"{error_msg} for {requirement}. Loosening constraints.")  # Debug print
                # Loosen the version constraints and retry
                success, error_msg = self.attempt_install(name)  # Retry without version spec
                if success:
                    print(f"{name} is installable after loosening version constraints")  # Debug print
                    return name, "LOOSEN", f"Package installable after loosening version constraints"
                else:
                    print(f"{name} still not installable: {error_msg}")  # Debug print
                    return name, "COMMENT", f"Package is not installable: {error_msg}"
            elif error_msg == "Package not found on PyPI":
                print(f"{requirement} not found on PyPI")  # Debug print
                return requirement, "COMMENT", "Package not found on PyPI"
            elif error_msg == "Python version incompatibility":
                print(f"{error_msg} for {requirement}")  # Debug print
                return requirement, "COMMENT", f"{error_msg}"
            else:
                # For any other installation failures
                print(f"Installation failed for {requirement}: {error_msg}")  # Debug print
                return requirement, "COMMENT", f"Installation failed: {error_msg}"



    def extract_python_version(self, error_output):
        """
        Extract the Python version range from the error output, if specified.

        This method uses a regular expression to search for Python version requirements in the installation error output.

        Args:
            error_output (str): The error output string from a failed installation attempt.

        Returns:
            str: A string representing the Python version range required by the package, or None if not found.
        """
        version_ranges = re.findall(r'Requires-Python ([^;]+);', error_output)
        if version_ranges:
            return ', '.join(version_ranges)
        return None
