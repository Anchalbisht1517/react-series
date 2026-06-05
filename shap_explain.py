import shap
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_appointments_v3.csv")
print("Data loaded:", df.shape)

X = df.drop('no_show', axis=1)
y = df['no_show']
print("Features:", X.columns.tolist())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

model = XGBClassifier(
    n_estimators=200, max_depth=6,
    learning_rate=0.1, scale_pos_weight=4, random_state=42)
model.fit(X_train, y_train)
print("✅ Model trained!")

explainer = shap.Explainer(model, X_train)
shap_values = explainer(X_test)
print("✅ SHAP values calculated!")

plt.figure()
shap.summary_plot(shap_values, X_test, plot_type="bar", show=False)
plt.title("Overall Feature Importance (SHAP)")
plt.tight_layout()
plt.show()

plt.figure()
shap.summary_plot(shap_values, X_test, show=False)
plt.title("SHAP Feature Impact")
plt.tight_layout()
plt.show()

print("\n--- Explaining Patient 0 ---")
print(X_test.iloc[0])
shap.plots.waterfall(shap_values[0], show=False)
plt.title("Why did model flag Patient 0?")
plt.tight_layout()
plt.show()
