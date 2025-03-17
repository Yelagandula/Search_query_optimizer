import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import ndcg_score

# Increase dataset size for better generalization
data = {
    "query_length": [5, 10, 3, 8, 6, 7, 4, 9, 2, 11, 12, 14, 15, 20, 25, 18, 22, 27, 30, 35],
    "click_rate": [0.7, 0.9, 0.4, 0.8, 0.6, 0.5, 0.3, 0.85, 0.2, 0.95, 0.15, 0.65, 0.75, 0.55, 0.45, 0.72, 0.82, 0.33, 0.62, 0.47],
    "rank_label": [1, 2, 5, 3, 4, 1, 3, 2, 5, 4, 3, 1, 2, 4, 5, 2, 1, 3, 4, 5],
    "qid": [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7]  # More query groups
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split into training & testing
X_train, X_test, y_train, y_test, qid_train, qid_test = train_test_split(
    df.drop(columns=["rank_label"]), df["rank_label"], df["qid"], test_size=0.3, random_state=42
)

# Define XGBoost Ranker with Regularization
params = {
    "objective": "rank:pairwise",
    "eval_metric": "ndcg",
    "booster": "gbtree",
    "eta": 0.05,  # Lower learning rate for better generalization
    "max_depth": 3,  # Prevent overfitting
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "lambda": 1.0,  # L2 Regularization
    "alpha": 0.7,  # L1 Regularization
}

# Implement 5-Fold Cross-Validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
ndcg_scores = []

for train_index, val_index in kf.split(X_train):
    X_train_cv, X_val_cv = X_train.iloc[train_index], X_train.iloc[val_index]
    y_train_cv, y_val_cv = y_train.iloc[train_index], y_train.iloc[val_index]
    qid_train_cv, qid_val_cv = qid_train.iloc[train_index], qid_train.iloc[val_index]

    # Convert to XGBoost DMatrix
    train_dmatrix = xgb.DMatrix(X_train_cv.drop(columns=["qid"]), label=y_train_cv)
    val_dmatrix = xgb.DMatrix(X_val_cv.drop(columns=["qid"]), label=y_val_cv)

    # Set groups
    train_dmatrix.set_group(qid_train_cv.value_counts().sort_index().tolist())
    val_dmatrix.set_group(qid_val_cv.value_counts().sort_index().tolist())

    # Train model using XGBoost's `train()` method
    evals = [(train_dmatrix, "train"), (val_dmatrix, "validation")]
    model = xgb.train(
        params,
        train_dmatrix,
        num_boost_round=150,  # Number of boosting rounds
        evals=evals,
        early_stopping_rounds=10,  # Stops training if no improvement
        verbose_eval=True
    )

    # Predict rankings for validation set
    y_pred_cv = model.predict(val_dmatrix)

    # Compute NDCG score
    ndcg = ndcg_score([y_val_cv], [y_pred_cv])
    ndcg_scores.append(ndcg)

# Print mean NDCG score across folds
mean_ndcg = np.mean(ndcg_scores)
print(f"Mean NDCG Score (5-Fold CV): {mean_ndcg:.4f}")

# Train final model on full dataset
train_dmatrix = xgb.DMatrix(X_train.drop(columns=["qid"]), label=y_train)
train_dmatrix.set_group(qid_train.value_counts().sort_index().tolist())
final_model = xgb.train(params, train_dmatrix, num_boost_round=200)

# Save trained model
final_model.save_model("query_ranker.model")
print("Final model trained and saved as query_ranker.model")
