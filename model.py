from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
import pickle

# Load MovieLens 100k
reader = Reader(line_format='user item rating timestamp', sep='\t')
data = Dataset.load_from_file('data/u.data', reader=reader)

# Build training set
trainset = data.build_full_trainset()

# Train SVD model
model = SVD()
model.fit(trainset)

# Save model
with open('svd_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as 'svd_model.pkl'")
