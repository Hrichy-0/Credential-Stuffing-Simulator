# Credential-Stuffing-Simulator: Unsupervised Machine Learning

## Overview
This project simulates a highly realistic banking API environment to generate, analyze, and classify synthetic network traffic. By building a custom multi-threaded orchestrator, I generated a balanced dataset of legitimate human users and malicious actors (Brute-Forcers and Password Sprayers). I then engineered behavioral features and deployed an Isolation Forest machine learning model to hunt the anomalies.

## 🏗️ Architecture & Methodology
1. **The Target (Flask):** Built a local banking API configured to log incoming request headers, IP addresses, and authentication statuses.
2. **The Cyber Range (Python/Concurrent Futures):** Engineered a multi-threaded traffic generator simulating three distinct behavioral profiles:
    * **Normal Humans:** Clumsy typing (20% typo rate), static IPs, single-account targeting.
    * **Brute-Force Bots:** High velocity, rapid IP rotation, massive unique username targeting.
    * **Password Sprayers:** "Low and slow" velocity, single password attempts across multiple accounts to evade basic rate-limiting.
3. **Feature Engineering (Pandas):** Extracted raw JSON logs and engineered advanced behavioral features, including Request Velocity (time between requests), Unique Account Targeting, and Failure Rates.
4. **Threat Hunting (Scikit-Learn):** Tuned an Unsupervised Isolation Forest algorithm to successfully separate legitimate customer noise from targeted cyber attacks.
5. **Exploratory Data Analysis (Seaborn/Plotly):** Mapped the AI's decision boundaries using 3D scatter plots, correlation heatmaps, and feature distribution boxplots.

## 📊 Key Findings & Visualizations
*(Upload your screenshots to the `images` folder and link them here)*
* **The Baseline Illusion:** Discovered and patched a logical flaw where the AI initially flagged high-volume humans as anomalies due to strict contamination constraints.
* **Feature Separation:** The Seaborn Pairplots proved that `unique_usernames` combined with `failure_rate` creates a near-perfect mathematical boundary for identifying credential stuffing.

## 🛠️ Tech Stack
* **Simulation:** Python, Flask, Concurrent Futures, Faker
* **Data Science:** Pandas, Scikit-Learn (Isolation Forest)
* **Data Visualization:** Plotly (3D Interactive), Seaborn, Matplotlib

### 📊 Key Findings & Visualizations

**3D Threat Landscape**
![3D Threat Landscape]([images/threat_landscape.png](https://github.com/Hrichy-0/Credential-Stuffing-Simulator/tree/main/images#:~:text=3Dthreatanalysis.png))

**Correlation Heatmap**
![Correlation Heatmap](images/correlation_heatmap.png)

**Threat Data Pairplot**
![Pairplot Matrix](images/pairplot_matrix.png)

