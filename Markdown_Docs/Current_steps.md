This is an excellent way to build. By treating this as a **"Technical Architect"** role, you ensure the code remains modular and "research-grade" rather than a tangled mess of AI-generated script.

Since you've already set up the folder structure, we will proceed in **three distinct sprints**.

---

### Sprint 1: Data Acquisition & Environment

A project is only as good as its data. Instead of random images, we will use **SWC files** (the industry standard for neuronal morphology) from **NeuroMorpho.Org**.

#### 1. The Dataset

We will use a small subset of rat hippocampal neurons.

* **Source:** [NeuroMorpho.org - Rat Hippocampal Neurons](https://www.google.com/search?q=-http://neuromorpho.org/byspecies.jsp%3Fspeciesname%3Drat)
* **Direct Download via Terminal:**
Run this in your terminal to create a sample data folder and download a real neuron structure:
```bash
mkdir -p data/raw
curl -L "http://neuromorpho.org/dwnid.jsp?neuron_name=cnic_001" -o data/raw/sample_neuron.swc

```



#### 2. Dependency Management

Create your `requirements.txt` to ensure "production-grade" reproducibility:

```text
numpy
pandas
opencv-python
scikit-image
plotly
pyyaml
pytest

```

**Next Step:** Run `pip install -r requirements.txt`.

---

### Sprint 2: The Core "Research" Logic

We will now implement the `ShollAnalyzer` class. To keep it professional, we use **Type Hinting** and **Docstrings**.

#### Step 1: The Preprocessor (`src/preprocessor.py`)

This script will convert the raw SWC data (coordinates) into a binary "skeleton" image that the Sholl analysis can actually read.

**Prompt to your AI:**

> "I have an SWC file at `data/raw/sample_neuron.swc`. Write a function in `src/preprocessor.py` called `swc_to_binary_mask`. It should:
> 1. Read the SWC file (skip lines starting with #).
> 2. Extract x, y coordinates.
> 3. Normalize coordinates to fit in a 1000x1000 numpy black image.
> 4. Draw lines between connected nodes using `cv2.line`.
> 5. Return the binary skeleton image as a numpy array."
> 
> 

#### Step 2: The Analyzer (`src/analyzer.py`)

Now, fill in the logic you started earlier.

**Prompt to your AI:**

> "Using the `ShollAnalyzer` skeleton provided in our previous discussion, implement the `_count_intersections` method.
> Logic:
> 1. Create a black mask of the same size as `self.image`.
> 2. Draw a white circle with `thickness=1` at `radius`.
> 3. Use `cv2.bitwise_and` to find where the circle and the neuron skeleton overlap.
> 4. Count the number of connected components in the resulting overlap to determine the number of intersections.
> 5. Ensure the code handles radii that extend beyond image boundaries gracefully."
> 
> 

---

### Sprint 3: Verification & Visualization

In research, a result isn't a result until it's plotted and tested.

#### 1. The Visualizer (`src/visualizer.py`)

**Prompt to your AI:**

> "Create a Plotly function in `src/visualizer.py` that takes the pandas DataFrame from `ShollAnalyzer.compute_profile()` and generates an interactive line chart.
> The chart should have:
> * X-axis: Radius ()
> * Y-axis: Number of Intersections
> * A 'Modern/Dark' template (using `plotly.io.templates`).
> * Save the output as `reports/figures/sholl_plot.html`."
> 
> 

#### 2. The "Circle Test" (`tests/test_analyzer.py`)

This is what makes it "production-grade".
**Prompt to your AI:**

> "Write a `pytest` file that creates a synthetic 500x500 image with a single white circle of radius 100. If I run `ShollAnalyzer` with a center at (250, 250), it should find 0 intersections for radius 50 and 2+ intersections for radius 100. This validates the logic."

---

### Summary of Your Immediate Tasks

1. **Terminal:** Run the `curl` command above to get your data.
2. **File Setup:** Save the `requirements.txt` and install it.
3. **AI Coding:** Use the **Sprint 2: Step 1** prompt to generate your first real piece of processing code.

**Would you like me to generate that "Research-Grade" README.md template now so you can track your progress visually on GitHub as you go?**