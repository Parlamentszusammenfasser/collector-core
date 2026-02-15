"""
Example collector module - demonstrates basic functionality
"""


class Collector:
    """Base collector class for parliamentary data collection"""
    
    def __init__(self, name: str):
        """
        Initialize a collector
        
        Args:
            name: Name of the collector
        """
        self.name = name
    
    def collect(self):
        """
        Collect data - to be implemented by subclasses
        
        Returns:
            dict: Collected data
        """
        return {"collector": self.name, "data": []}
