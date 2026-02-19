# PySholl-Pro: Automated Dendritic Morphology Analysis 🧠

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

PySholl-Pro is a high-performance, automated Python pipeline for conducting Sholl Analysis on neuronal morphologies. It bridges the gap between raw biological data (SWC format) and publication-ready quantitative insights.

## 📖 The Science: Sholl Analysis
Sholl analysis is a quantitative method used in neurobiology to measure the morphological complexity of neurons. 

The algorithm centers a series of concentric circles (or spheres in 3D) on the neuronal soma. It then calculates the number of dendritic intersections $N$ as a function of the radial distance $r$ from the soma. 

The intersection profile is defined as:
$$N(r) = \sum_{i} \delta(r - r_i)$$
Where $\delta$ represents an intersection event at a given radius $r_i$. This provides a mathematical signature of a neuron's branching density and overall reach.

## ⚙️ Features
* **Automated Preprocessing:** Converts standard coordinate-based `.swc` files into normalized, skeletonized 2D binary masks.
* **Mathematical Precision:** Utilizes OpenCV connected-component analysis to accurately count distinct dendritic branches, preventing artificial inflation from thick dendrites.
* **Interactive Visualization:** Generates responsive, dark-themed HTML plots using `plotly` for immediate exploratory data analysis.
* **Configuration-Driven:** Fully decoupled logic via YAML configs, ensuring high reproducibility.

## 🚀 Quick Start

### 1. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/yourusername/PySholl-Pro.git](https://github.com/yourusername/PySholl-Pro.git)
cd PySholl-Pro
pip install -r requirements.txt
```

### 2. Data Acquisition
Place your standard .swc files into the data/raw/ directory. High-quality neuronal reconstructions can be downloaded freely from NeuroMorpho.Org.

### 3. Execution
Run the automated pipeline via the main entry point:
```python 
python main.py
```
This will automatically:

- Parse the SWC and generate a binary skeleton in data/processed/.
- Compute the Sholl profile and output a CSV in data/results/.
- Generate an interactive HTML visualization in reports/figures/.


### 4. 📂 Repository Structure
```
PySholl-Pro/
├── configs/             # YAML configuration files
├── data/
│   ├── raw/             # Input SWC files
│   ├── processed/       # Skeletonized binary masks
│   └── results/         # Output CSV data
├── reports/
│   └── figures/         # Interactive HTML plots
├── src/                 # Core source code
│   ├── analyzer.py      # Mathematical intersection logic
│   ├── preprocessor.py  # SWC parsing and image normalization
│   └── visualizer.py    # Plotly graph generation
├── main.py              # Pipeline entry point
└── requirements.txt     # Dependency lockfile
```

### 📄 License
This project is licensed under the MIT License.