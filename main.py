import yaml
from src.preprocessor import swc_to_binary_mask
from src.analyzer import ShollAnalyzer
from src.visualizer import plot_sholl_profile
import cv2
import os

def run_pipeline(config_path="configs/default_config.yaml"):
    with open(config_path, 'r') as f:
        cfg = yaml.safe_load(f)

    # 1. Preprocess
    print("--- Step 1: Preprocessing ---")
    mask = swc_to_binary_mask(cfg['paths']['raw_data'], padding=cfg['analysis']['padding'])
    cv2.imwrite(cfg['paths']['processed_mask'], mask)

    # 2. Analyze
    print("--- Step 2: Analyzing ---")
    analyzer = ShollAnalyzer(
        mask, 
        start_radius=cfg['analysis']['start_radius'], 
        step_size=cfg['analysis']['step_size']
    )
    results = analyzer.compute_profile()
    results.to_csv(cfg['paths']['results_csv'], index=False)

    # 3. Visualize
    print("--- Step 3: Visualizing ---")
    plot_sholl_profile(cfg['paths']['results_csv'], cfg['paths']['report_html'])
    print(f"Pipeline Complete. View your results here: {cfg['paths']['report_html']}")

if __name__ == "__main__":
    run_pipeline()