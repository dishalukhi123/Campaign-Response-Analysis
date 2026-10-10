
from pathlib import Path
import numpy as np
import pandas as pd

# Create the dataset folder
DATA = Path("data/raw/set_d.csv")
DATA.parent.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
rng = np.random.default_rng(RANDOM_STATE)

# Generate 300 records
n = 300

visits = rng.poisson(5, n).astype(float)
recency = rng.integers(1, 91, n).astype(float)

engagement = np.clip(
    rng.normal(50 + visits * 2 - recency * 0.12, 12, n),
    0, 100
)

spend = np.maximum(
    0, rng.gamma(2.2, 450, n) + visits * 35 + engagement * 3
)

group = rng.choice(["G1", "G2"], size=n, p=[0.52, 0.48])

logit = (
    -2.2 + 0.20 * visits + 0.035 * engagement
    - 0.012 * recency + (group == "G2") * 0.30
)

probability = 1 / (1 + np.exp(-logit))
response = rng.binomial(1, probability)

# Create DataFrame
df = pd.DataFrame({
    "record_id": [f"R{i+1:03d}" for i in range(n)],
    "visits": visits,
    "recency": recency,
    "engagement": engagement,
    "spend": spend,
    "group": group,
    "response": response
})

# Add a few missing values for data-cleaning practice
for col in ["visits", "engagement", "spend"]:
    missing_idx = rng.choice(n, size=3, replace=False)
    df.loc[missing_idx, col] = np.nan

# Save the CSV dataset
df.to_csv(DATA, index=False)

print("Dataset created successfully!")
print("File location:", DATA.resolve())
print("Dataset shape:", df.shape)
print(df.head())
