import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("cleaned_appointments_v3.csv")
print("Data loaded:", df.shape)

# Set style
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Patient No-Show EDA Dashboard", fontsize=18, fontweight='bold')

# Chart 1 - No-show vs Show-up count
ax1 = axes[0, 0]
counts = df['no_show'].value_counts()
ax1.bar(['Showed Up', 'No-Show'], counts.values, color=['steelblue', 'tomato'])
ax1.set_title('Show-up vs No-Show Count')
ax1.set_ylabel('Number of Patients')
for i, v in enumerate(counts.values):
    ax1.text(i, v + 200, str(v), ha='center', fontweight='bold')

# Chart 2 - No-show by age group
ax2 = axes[0, 1]
age_noshow = df.groupby('age_group')['no_show'].mean() * 100
# After
labels = ['Child\n(0-12)', 'Teen\n(13-18)', 'Adult\n(19-35)', 'Senior\n(36-60)', 'Elderly\n(60+)', 'Other']
ax2.bar(labels[:len(age_noshow)], age_noshow.values, color='coral')
ax2.bar(labels[:len(age_noshow)], age_noshow.values, color='coral')
ax2.set_title('No-Show Rate by Age Group')
ax2.set_ylabel('No-Show Rate (%)')

# Chart 3 - SMS impact
ax3 = axes[0, 2]
sms_noshow = df.groupby('sms_received')['no_show'].mean() * 100
ax3.bar(['No SMS', 'SMS Received'], sms_noshow.values, color=['tomato', 'seagreen'])
ax3.set_title('No-Show Rate: SMS vs No SMS')
ax3.set_ylabel('No-Show Rate (%)')
for i, v in enumerate(sms_noshow.values):
    ax3.text(i, v + 0.3, f'{v:.1f}%', ha='center', fontweight='bold')

# Chart 4 - No-show by day of week
ax4 = axes[1, 0]
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_noshow = df.groupby('appointment_weekday')['no_show'].mean() * 100
ax4.bar(days[:len(day_noshow)], day_noshow.values, color='mediumpurple')
ax4.set_title('No-Show Rate by Day of Week')
ax4.set_ylabel('No-Show Rate (%)')
ax4.tick_params(axis='x', rotation=45)

# Chart 5 - Days waiting distribution
ax5 = axes[1, 1]
df[df['days_waiting'] <= 60]['days_waiting'].hist(bins=30, ax=ax5, color='steelblue', edgecolor='white')
ax5.set_title('Days Waiting Distribution')
ax5.set_xlabel('Days Waiting')
ax5.set_ylabel('Number of Patients')

# Chart 6 - No-show rate by waiting time
ax6 = axes[1, 2]
df['wait_bucket'] = pd.cut(df['days_waiting'], bins=[0,7,14,30,60,200], labels=['0-7','8-14','15-30','31-60','60+'])
wait_noshow = df.groupby('wait_bucket', observed=True)['no_show'].mean() * 100
ax6.bar(wait_noshow.index, wait_noshow.values, color='darkorange')
ax6.set_title('No-Show Rate by Waiting Time')
ax6.set_xlabel('Days Waiting')
ax6.set_ylabel('No-Show Rate (%)')

plt.tight_layout()
plt.show()
print("✅ EDA Dashboard complete!")