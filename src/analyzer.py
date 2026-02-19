import numpy as np
import pandas as pd
import cv2
from typing import Tuple, List, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class ShollAnalyzer:
    """
    Handles the mathematical counting of dendritic intersections 
    at increasing radial distances from the soma.
    """
    def __init__(self, image: np.ndarray, center: Optional[Tuple[int, int]] = None, 
                 start_radius: int = 10, step_size: int = 10):
        """
        :param image: Binary skeleton image (255 for dendrite, 0 for background)
        :param center: (x, y) coordinates of the soma. If None, uses image center.
        :param start_radius: Distance from center to start the first circle.
        :param step_size: Distance between consecutive circles.
        """
        self.image = image
        self.center = center or (image.shape[1] // 2, image.shape[0] // 2)
        self.start_radius = start_radius
        self.step_size = step_size
        self.max_radius = self._calculate_max_radius()

    def _calculate_max_radius(self) -> int:
        """Determines the furthest possible radius within the image bounds."""
        h, w = self.image.shape
        corners = [(0, 0), (w, 0), (0, h), (w, h)]
        distances = [np.sqrt((c[0]-self.center[0])**2 + (c[1]-self.center[1])**2) for c in corners]
        return int(max(distances))

    def _count_intersections(self, radius: int) -> int:
        """
        Core Logic: Draws a circle mask and finds overlaps with the neuron skeleton.
        """
        # Create a blank mask for the circle
        mask = np.zeros_like(self.image)
        
        # Draw the circle with thickness=1 to ensure we only catch the boundary
        cv2.circle(mask, self.center, radius, 255, thickness=1)
        
        # Logical AND to find where the circle hits the skeleton
        intersection_points = cv2.bitwise_and(self.image, mask)
        
        # Count connected components. 
        # Each 'blob' of white pixels is one intersection.
        num_labels, _ = cv2.connectedComponents(intersection_points)
        
        # subtract 1 because label 0 is the background
        count = max(0, num_labels - 1)
        return count

    def compute_profile(self) -> pd.DataFrame:
        """
        Iterates through radii and compiles the Sholl profile data.
        """
        logging.info(f"Computing Sholl profile from radius {self.start_radius} to {self.max_radius}")
        
        radii = list(range(self.start_radius, self.max_radius, self.step_size))
        intersections = []
        
        for r in radii:
            count = self._count_intersections(r)
            intersections.append(count)
            
        df = pd.DataFrame({
            'radius': radii,
            'intersections': intersections
        })
        
        logging.info("Sholl analysis complete.")
        return df

if __name__ == "__main__":
    # Integration Test: Run this after running preprocessor.py
    import os
    mask_path = "data/processed/skeleton_mask.png"
    
    if os.path.exists(mask_path):
        # Load the mask we created in Step 1
        skeleton = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        analyzer = ShollAnalyzer(skeleton, step_size=20)
        results = analyzer.compute_profile()
        
        # Save results to CSV for record keeping
        os.makedirs("data/results", exist_ok=True)
        results.to_csv("data/results/sholl_data.csv", index=False)
        print(results.head(10))
    else:
        logging.error("Could not find skeleton_mask.png. Run preprocessor.py first.")