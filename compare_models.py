import matplotlib.pyplot as plt
import numpy as np

# Results from both models
models = ['Random Forest', 'XGBoost']

accuracy  = [0.60, 0.62]
precision = [0.72, 0.72]
recall    = [0.60, 0.62]
f1        = [0.64, 0.66]

x = np.arange(len(models))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(x - 0.3, accuracy,  width, label='Accuracy',  color='steelblue')
ax.bar(x - 0.1, precision, width, label='Precision', color='seagreen')
ax.bar(x + 0.1, recall,    width, label='Recall',    color='orange')
ax.bar(x + 0.3, f1,        width, label='F1 Score',  color='tomato')

ax.set_ylim(0, 1)
ax.set_ylabel('Score')
ax.set_title('Random Forest vs XGBoost — Model Comparison')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()