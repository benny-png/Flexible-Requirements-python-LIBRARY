import logging
import time
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class FlexibleRequirementsGenerator:
    def __init__(self, checker, concurrent=True):
        self.checker = checker
        self.concurrent = concurrent

    def process_requirements(self, requirements):
        if self.concurrent:
            return self._process_requirements_concurrent(requirements)
        else:
            return self._process_requirements_sequential(requirements)

    def _process_requirements_concurrent(self, requirements):
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_req = {executor.submit(self.checker.check_compatibility, req): req for req in requirements}
            for future in as_completed(future_to_req):
                try:
                    results.append(future.result())
                except Exception as e:
                    print(f"Error processing {future_to_req[future]}: {str(e)}")  # Debug print
                    results.append((future_to_req[future], "KEEP", f"Error processing: {str(e)}"))
        return results

    def _process_requirements_sequential(self, requirements):
        return [self.checker.check_compatibility(req) for req in requirements]

    def generate_flexible_requirements(self, input_file, output_file):
        logger.info(f"Starting to process {input_file}")
        with open(input_file, 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        
        print(f"Read {len(requirements)} requirements from {input_file}")  # Debug print

        start_time = time.time()
        results = self.process_requirements(requirements)
        end_time = time.time()

        print(f"Processed {len(results)} requirements in {end_time - start_time:.2f} seconds")  # Debug print

        with open(output_file, 'w') as f:
            f.write(f"# Generated for Python {platform.python_version()} on {platform.system()}\n")
            for req, action, message in results:
                if action == "KEEP":
                    f.write(f"{req}\n")
                elif action == "LOOSEN":
                    f.write(f"{req}\n")
                elif action == "COMMENT":
                    f.write(f"# {req}  # {message}\n")
                f.write(f"# {message}\n")
        
        logger.info(f"Processing completed in {end_time - start_time:.2f} seconds")
        logger.info(f"Flexible requirements written to {output_file}")
        print(f"Flexible requirements written to {output_file}")  # Debug print
