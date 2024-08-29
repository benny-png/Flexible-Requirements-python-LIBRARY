from abc import ABC, abstractmethod

class CompatibilityChecker(ABC):
    @abstractmethod
    def check_compatibility(self, requirement):
        pass