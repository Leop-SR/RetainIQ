import secrets
import pandas as pd

feature_usage = pd.read_csv('../data/raw/ravenstack_feature_usage.csv')

# Store all existing IDs
existing_ids = set(feature_usage["usage_id"])

# Find duplicated rows (excluding the first occurrence)
duplicate_mask = feature_usage["usage_id"].duplicated(keep="first")

def generate_usage_id(existing_ids):
    while True:
        new_id = f"U-{secrets.token_hex(3)}"

        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id

# Replace duplicated IDs
for idx in feature_usage[duplicate_mask].index:
    feature_usage.at[idx, "usage_id"] = generate_usage_id(existing_ids)

# -------------------------
# VALIDATION
# -------------------------

assert feature_usage["usage_id"].is_unique, \
    "Duplicate IDs still exist!"

print("✅ Duplicate ID issue solved successfully.")

feature_usage.to_csv('../data/raw/ravenstack_feature_usage.csv',index=False)