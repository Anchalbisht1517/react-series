from setuptools import find_packages, setup

setup(
    name="noshow_predictor",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Medical appointment no-show prediction system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "xgboost",
        "imbalanced-learn",
        "joblib",
        "streamlit",
        "plotly",
        "shap",
        "pyyaml",
    ],
)
