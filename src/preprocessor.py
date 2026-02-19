import os
import numpy as np
import cv2
import pandas as pd
from typing import Tuple, Optional
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def load_swc(file_path: str) -> pd.DataFrame:
    """
    Reads an SWC file into a Pandas DataFrame.
    Professional SWC files often have headers starting with '#'.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SWC file not found at: {file_path}")
    
    columns = ['id', 'type', 'x', 'y', 'z', 'radius', 'parent']
    try:
        df = pd.read_csv(file_path, sep=r'\s+', comment='#', names=columns)
        logging.info(f"Successfully loaded SWC with {len(df)} nodes.")
        return df
    except Exception as e:
        logging.error(f"Failed to parse SWC file: {e}")
        raise

def swc_to_binary_mask(swc_path: str, img_size: Tuple[int, int] = (1000, 1000), 
                        padding: int = 50) -> np.ndarray:
    """
    Converts SWC coordinates into a 2D binary skeleton image.
    Uses normalization to fit the neuron within the specified image size.
    """
    df = load_swc(swc_path)
    
    # 1. Normalize Coordinates to fit img_size
    # We ignore Z-axis for a 2D Sholl Analysis
    min_x, max_x = df['x'].min(), df['x'].max()
    min_y, max_y = df['y'].min(), df['y'].max()
    
    # Calculate scale to preserve aspect ratio
    width = max_x - min_x
    height = max_y - min_y
    scale = (min(img_size) - 2 * padding) / max(width, height)
    
    # Apply scaling and centering
    df['norm_x'] = ((df['x'] - min_x) * scale + padding).astype(int)
    df['norm_y'] = ((df['y'] - min_y) * scale + padding).astype(int)
    
    # 2. Create Blank Canvas (Black Background)
    mask = np.zeros(img_size, dtype=np.uint8)
    
    # 3. Draw the Skeleton
    # SWC parent link: -1 means root, otherwise it's the ID of the parent node
    node_map = {int(row.id): (int(row.norm_x), int(row.norm_y)) for row in df.itertuples()}
    
    for row in df.itertuples():
        parent_id = int(row.parent)
        if parent_id in node_map:
            start_point = node_map[parent_id]
            end_point = (int(row.norm_x), int(row.norm_y))
            # Draw line with white (255) and thickness 1 (skeletonized)
            cv2.line(mask, start_point, end_point, 255, thickness=1)
            
    logging.info(f"Generated binary mask of size {img_size}")
    return mask

if __name__ == "__main__":
    # Test block to verify Step 1
    input_path = "data/raw/cnic_001.CNG.swc"
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        binary_image = swc_to_binary_mask(input_path)
        cv2.imwrite(os.path.join(output_dir, "skeleton_mask.png"), binary_image)
        logging.info("Test successful: Saved mask to data/processed/skeleton_mask.png")
    except Exception as e:
        logging.error(f"Test failed: {e}")