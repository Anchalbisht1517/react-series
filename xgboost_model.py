import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import joblib

# Load NEW cleaned data
df = pd.read_csv("cleaned_appointments_v3.csv")

print("Columns:", df.columns.tolist())
print("Shape:", df.shape)

# Features and target
X = df.drop('no_show', axis=1)
y = df['no_show']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train XGBoost
model_xgb = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=4,
    random_state=42
)

model_xgb.fit(X_train, y_train)

# Evaluate at 0.5
y_pred = model_xgb.predict(X_test)
print("\n=== Results at 0.5 threshold ===")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2%}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens')
plt.title('XGBoost V2 Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Feature importance
importances = pd.Series(model_xgb.feature_importances_, index=X.columns)
importances.sort_values().plot(kind='barh', color='steelblue')
plt.title('Feature Importance V2')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.show()

# Save
joblib.dump(model_xgb, 'xgboost_model_v2.pkl')
print("✅ New model saved!")