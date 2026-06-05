import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("cleaned_appointments.csv")
df['gender'] = df['gender'].map({'F': 0, 'M': 1})
df.drop(columns=['scheduledday', 'appointmentday', 'neighbourhood'], inplace=True)

X = df.drop('no_show', axis=1)
y = df['no_show']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = XGBClassifier(scale_pos_weight=4, random_state=42)
model.fit(X_train, y_train)

# Get probabilities instead of just 0/1
y_proba = model.predict_proba(X_test)[:, 1]

# Try different thresholds
thresholds = [0.2, 0.3, 0.4, 0.5, 0.6]

for t in thresholds:
    y_pred = (y_proba >= t).astype(int)
    report = classification_report(y_test, y_pred, output_dict=True)
    print(f"\nThreshold: {t}")
    print(f"  No-show Recall:    {report['1']['recall']:.2f}")
    print(f"  No-show Precision: {report['1']['precision']:.2f}")
    print(f"  Accuracy:          {report['accuracy']:.2f}")

# Plot threshold vs recall
recalls = []
precisions = []
thresholds_range = np.arange(0.1, 0.9, 0.05)

for t in thresholds_range:
    y_pred = (y_proba >= t).astype(int)
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    recalls.append(report['1']['recall'])
    precisions.append(report['1']['precision'])

plt.figure(figsize=(10, 5))
plt.plot(thresholds_range, recalls, label='Recall (catches no-shows)', color='orange')
plt.plot(thresholds_range, precisions, label='Precision (accuracy of alerts)', color='steelblue')
plt.axvline(x=0.3, color='red', linestyle='--', label='Recommended threshold (0.3)')
plt.xlabel('Threshold')
plt.ylabel('Score')
plt.title('Finding the Best Threshold')
plt.legend()
plt.grid(True)
plt.show()