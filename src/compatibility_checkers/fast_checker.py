# src/compatibility_checkers/fast_checker.py
from .base import CompatibilityChecker
from ..parsers import parse_requirement
from ..package_info import get_package_info
from ..utils import is_valid_version
from packaging import specifiers, version

class FastCompatibilityChecker(CompatibilityChecker):
    def check_compatibility(self, requirement):
        print(f"Checking compatibility for: {requirement}")  # Debug print
        name, version_spec = parse_requirement(requirement)
        if not name:
            print(f"Invalid requirement format: {requirement}")  # Debug print
            return requirement, "KEEP", "Invalid requirement format"

        package_info = get_package_info(name)
        if not package_info:
            print(f"Package not found on PyPI: {name}")  # Debug print
            return requirement, "COMMENT", f"Package not found on PyPI"

        if not version_spec:
            print(f"No version specified for: {name}")  # Debug print
            return requirement, "KEEP", "No version specified"

        try:
            spec = specifiers.SpecifierSet(version_spec)
            valid_versions = [v for v in package_info['releases'].keys() if is_valid_version(v)]
            
            # Check Python version compatibility
            current_python_version = version.parse(f"{package_info['info']['requires_python']}")
            compatible_versions = []
            for v in valid_versions:
                release_info = package_info['releases'][v]
                if release_info:
                    python_requires = release_info[0].get('requires_python')
                    if python_requires and current_python_version in specifiers.SpecifierSet(python_requires):
                        if v in spec:
                            compatible_versions.append(v)
            
            print(f"Compatible versions for {name}: {compatible_versions}")  # Debug print
            if compatible_versions:
                return requirement, "KEEP", f"Compatible versions found: {', '.join(compatible_versions[:3])}..."
            else:
                print(f"No compatible versions found for {name}")  # Debug print
                if valid_versions:
                    return requirement, "COMMENT", "No compatible versions found for the current Python version"
                else:
                    return requirement, "COMMENT", "No versions found that satisfy the requirement"
        except specifiers.InvalidSpecifier:
            print(f"Invalid version specifier for {name}: {version_spec}")  # Debug print
            return requirement, "KEEP", "Invalid version specifier"
        except Exception as e:
            print(f"Error checking compatibility for {requirement}: {str(e)}")  # Debug print
            return requirement, "KEEP", f"Error checking compatibility: {str(e)}"