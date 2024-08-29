import argparse
import logging
from src.compatibility_checkers.fast_checker import FastCompatibilityChecker
from src.compatibility_checkers.installation_checker import InstallationCompatibilityChecker
from src.generator import FlexibleRequirementsGenerator

def main():
    parser = argparse.ArgumentParser(description="Generate flexible requirements file")
    parser.add_argument("input", nargs="?", default="requirements.txt", help="Input requirements file")
    parser.add_argument("output", nargs="?", default="flexible_requirements.txt", help="Output flexible requirements file")
    parser.add_argument("--sequential", action="store_true", help="Use sequential processing instead of concurrent")
    parser.add_argument("--fast", action="store_true", help="Use fast compatibility checking without installation attempts")
    parser.add_argument("--log", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help="Set the logging level")
    args = parser.parse_args()

    logging.basicConfig(level=args.log, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    print(f"Arguments: {args}")  # Debug print

    logger.info(f"Using input file: {args.input}")
    logger.info(f"Output will be written to: {args.output}")
    logger.info(f"Using {'sequential' if args.sequential else 'concurrent'} processing")
    logger.info(f"Using {'fast' if args.fast else 'installation-based'} compatibility checking")

    checker = FastCompatibilityChecker() if args.fast else InstallationCompatibilityChecker()
    generator = FlexibleRequirementsGenerator(checker, not args.sequential)
    generator.generate_flexible_requirements(args.input, args.output)

if __name__ == "__main__":
    main()