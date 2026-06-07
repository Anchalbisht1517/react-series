# 🏥 Medical Appointment No-Show Predictor

End-to-end machine learning system to predict and explain medical appointment no-shows.

## 🚀 Live Demo

**[Your app on Streamlit Cloud](https://your-app-name.streamlit.app)** *(replace after deployment)*

---

## 📋 Dataset Source

- **KaggleV2-May-2016.csv** — [Medical Appointment No Shows dataset](https://www.kaggle.com/datasets/joniarroba/noshowappointments)
- ~110,527 rows × 14 columns
- Target: `No-show` (Yes = missed, No = attended)

---

## 🛠️ Tech Stack

| Layer | Tools |
|-------|-------|
| Data & ML | Python, pandas, NumPy, scikit-learn, XGBoost, imbalanced-learn |
| Explainability | SHAP |
| App & Viz | Streamlit, Plotly, Matplotlib, Seaborn |
| Config | YAML |

---

## 📊 Key Metrics (XGBoost — Primary Model)

| Metric | Target | Notes |
|--------|--------|-------|
| **Recall** | ≥ 0.70 | Primary — catch as many no-shows as possible |
| Precision | ~0.30–0.40 | Acceptable trade-off for high recall |
| F1-Score | ~0.45–0.50 | Balanced view |
| ROC-AUC | ~0.70–0.75 | Discrimination power |

*SMOTE + `scale_pos_weight=4` used to address ~20% class imbalance.*

---

## 🏗️ Project Structure

```
noshow_predictor/
├── app.py                          # Streamlit entry point
├── config/                         # YAML configs
│   ├── config.yaml
│   ├── params.yaml
│   └── schema.yaml
├── data/
│   ├── raw/                        # Your CSV goes here
│   └── processed/
├── notebooks/                      # Your .ipynb files
├── src/
│   └── noshow/
│       ├── components/             # Data pipeline + model trainer + evaluation + SHAP
│       ├── pipeline/               # Prediction pipeline
│       └── visualization/          # EDA, evaluation, SHAP plot helpers
├── pages/                          # Streamlit multi-page app
│   ├── 1_Dashboard.py
│   ├── 2_Single_Patient_Check.py
│   ├── 3_Batch_Upload.py
│   ├── 4_Model_Performance.py
│   └── 5_SHAP_Explainability.py
├── models/                         # Saved artifacts (.pkl, .json)
├── outputs/
│   └── plots/                      # Generated charts
├── tests/                          # Unit tests
├── requirements.txt
└── setup.py
```

---

## ⚙️ Local Setup

```bash
# 1. Clone repo
git clone https://github.com/your-username/noshow_predictor.git
cd noshow_predictor

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
# source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install project in editable mode
pip install -e .

# 5. Place dataset
# Copy KaggleV2-May-2016.csv into data/raw/

# 6. Run training pipeline (optional — if model artifacts missing)
python -m src.noshow.components.data_ingestion
python -m src.noshow.components.data_validation
python -m src.noshow.components.data_cleaning
python -m src.noshow.components.feature_engineering
python -m src.noshow.components.data_transformation
python -m src.noshow.components.model_trainer
python -m src.noshow.components.model_evaluation
python -m src.noshow.components.explainability

# 7. Launch Streamlit app
streamlit run app.py
```

---

## 🧪 Tests

```bash
python -m unittest discover tests
```

---

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/your-username/noshow_predictor.git
   git push -u origin main
   ```

2. **Connect to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click **New app**
   - Select your GitHub repo `noshow_predictor`
   - Set **Main file path** to `app.py`
   - Click **Deploy**

3. **Advanced Settings** (if needed)
   - Python version: `3.9` or higher
   - Ensure `requirements.txt` is at repo root

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `models/xgboost_model_v2.pkl` | Primary trained model |
| `models/preprocessor.pkl` | Fitted StandardScaler |
| `models/feature_names.json` | Exact feature order for inference alignment |
| `outputs/model_comparison.csv` | All model metrics |
| `outputs/plots/` | EDA + evaluation + SHAP images |

---

## ⚠️ Notes

- **No extra notebooks or CSVs** are included in this repo. Please place your own `.ipynb` files in `notebooks/` and raw data in `data/raw/`.
- `.gitignore` excludes `data/raw/`, `models/*.pkl`, and `.streamlit/secrets.toml`.
- If `models/*.pkl` files exceed 100 MB, use [Git LFS](https://git-lfs.github.com/).

---

## 📬 Contact

Created by **Your Name** — feel free to open an issue or PR.
