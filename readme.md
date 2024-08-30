
# Flexible Requirements Generator

This tool generates a flexible `requirements.txt` file from an existing one, helping to resolve version conflicts and compatibility issues in Python projects.

[View on PyPI](https://pypi.org/project/flexible-requirements) (Note: PyPI version may have issues)

## Real-Life Use Cases

Perfect for teams where each member uses different Python versions, operating systems, or hardware, this tool ensures that the `requirements.txt` file remains flexible and compatible across all environments, resolving version conflicts and platform-specific issues.

## Features

- Checks package compatibility with PyPI without installing packages
- Supports both concurrent and sequential processing
- Keeps compatible requirements, loosens incompatible ones, and comments out unavailable packages
- Provides detailed information about each requirement's status
- Handles platform-specific package availability
- Includes comprehensive logging for better visibility and debugging

## Installation

1. Clone this repository and install the dependencies manually:
   ```
   git clone https://github.com/benny-png/Flexible-Requirements-python-LIBRARY.git
   cd Flexible-Requirements-python-LIBRARY
   pip install -r own_requirements.txt
   ```

2. Alternatively, you can install the package from PyPI (note: this method may have issues):
   ```
   pip install flexible-requirements
   ```

## Usage

Run the script from the command line:

### Default Usage
```
python main.py
```

### Modular Usage
```
python main.py [input_file] [output_file] [--sequential] [--fast] [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
```
- `input_file`: Path to the input requirements file (default: `requirements.txt`)
- `output_file`: Path to the output flexible requirements file (default: `flexible_requirements.txt`)
- `--sequential`: Use sequential processing instead of concurrent (optional)
- `--log`: Set the logging level (default: INFO)
- `--fast`: Faster but not that accurate and not perfected yet/tested well

### Example
```
python main.py my_requirements.txt my_flexible_requirements.txt --sequential --log DEBUG --fast
```

## How it works

1. The script reads the input requirements file.
2. For each requirement, it checks the package's availability and version compatibility using the PyPI JSON API.
3. It considers the current platform (e.g., Windows, Linux, macOS) when checking for compatible versions.
4. Based on the results, it either:
   - Keeps the requirement as-is if it's compatible
   - Loosens the version constraint if no compatible version is found for the current platform
   - Comments out the requirement if the package is not available on PyPI or for the current platform
5. The processed requirements are written to the output file with explanatory comments.
6. Detailed logs are provided throughout the process for better visibility and debugging.

## Output

The generated flexible requirements file includes:
- The original requirements (kept, loosened, or commented out)
- Comments explaining the status of each requirement
- Information about compatible versions or reasons for changes

## Performance

The script supports both concurrent and sequential processing. Concurrent processing is faster but may be limited by API rate limits. Sequential processing is slower but more reliable for large requirement files.

## Limitations

- Relies on the PyPI JSON API, so it requires an internet connection
- Does not handle dependencies of packages, only direct requirements
- May be affected by PyPI API rate limits when processing large files concurrently
- Platform-specific package availability may result in different outputs on different systems

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
