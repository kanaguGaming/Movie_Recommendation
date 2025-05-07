import pandas as pd

# Load user info
columns = ['userId', 'age', 'gender', 'occupation', 'zip_code']
users = pd.read_csv('data/u.user', sep='|', names=columns)

# Save to a clean file
users.to_csv('users.csv', index=False)

print("✅ Processed and saved clean 'users.csv'")
