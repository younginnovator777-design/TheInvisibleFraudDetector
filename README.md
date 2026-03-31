# 🕵️‍♂️ The Invisible Fraud Detector
**Real-Time AI for False-Positive Reduction in Digital Payments**

## 📌 Overview
Traditional fraud detection systems rely on rigid rules, resulting in up to 90% false-positive rates that block genuine transactions. **The Invisible Fraud Detector** replaces static rules with a dynamic, privacy-first scoring engine. By analyzing transaction behavior and structural topology, it accurately identifies hidden money mule rings while dramatically reducing false alerts.

## 🧠 The Triple-Engine Architecture
Our system evaluates each transaction through three distinct lenses to calculate a unified, weighted threat score:
1. **Engine A (Behavioral Math):** Calculates "Drain Rates" to distinguish between normal business volume and money mule liquidation.
2. **Engine B (Machine Learning):** Utilizes `IsolationForest` for multi-dimensional statistical outlier detection.
3. **Engine C (Graph Theory):** Leverages `NetworkX` to map node-edge topologies, instantly exposing circular money flows and hidden hubs.

## 🛠️ Tech Stack
* **Model Training & Pipeline:** Google Colab, Pandas, Scikit-Learn, NetworkX
* **Interactive Dashboard:** Streamlit, Plotly
* **Explainable AI:** Dynamic Reason Generation (Translating math into actionable insights)

## 📂 Repository Structure
* `app.py`: The main Streamlit dashboard application.
* `dashboard_dataV2.csv`: The processed, scored dataset ready for live analysis.
* `TheInvisibleFraudDetector.ipynb`: The core research, engine logic, and data processing notebook.
* `requirements.txt`: Environment dependencies.

## 🚀 How to Run Locally
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt