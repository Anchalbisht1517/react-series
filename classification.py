import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("cleaned_appointments.csv")

# Check all columns
print(df.dtypes)

# Encode gender
df['gender'] = df['gender'].map({'F': 0, 'M': 1})

# Drop date columns and text columns
df.drop(columns=['scheduledday', 'appointmentday', 'neighbourhood'], inplace=True)

# Features and target
X = df.drop('no_show', axis=1)
y = df['no_show']

print("Columns used for training:", X.columns.tolist())

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()
# Feature Importance
importances = pd.Series(model.feature_importances_, index=X.columns)
importances.sort_values().plot(kind='barh', color='steelblue')
plt.title('What factors affect no-shows?')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.show()
import joblib

# Save the model
joblib.dump(model, 'noshow_model.pkl')
print("✅ Model saved as noshow_model.pkl")