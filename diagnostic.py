import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import learning_curve, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# 1. LOAD AND PREPARE DATA
try:
    df = pd.read_csv('telecom_churn.csv') 
    
    # Correcting the target column name based on your file
    target_col = 'churned' 
    
    # Preprocessing
    # Drop customer_id as it's just an identifier, and the target column
    X = df.drop(['customer_id', target_col], axis=1)
    y = df[target_col]
    
    # Convert categorical to dummy variables (gender, internet_service, etc.)
    X = pd.get_dummies(X, drop_first=True)
    
    # Scaling (Crucial for Logistic Regression)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    print("Data loaded and preprocessed successfully using 'churned' as target.")
except FileNotFoundError:
    print("Error: Dataset file not found in 'data/' folder.")
    exit()
except KeyError as e:
    print(f"Error: Column not found {e}. Check your CSV headers.")
    exit()

def generate_learning_curve(X, y):
    model = LogisticRegression(max_iter=1000)
    cv = StratifiedKFold(n_splits=5)

    # 2. Compute learning curve scores
    train_sizes, train_scores, val_scores = learning_curve(
        estimator=model,
        X=X,
        y=y,
        train_sizes=np.linspace(0.1, 1.0, 5),
        cv=cv,
        scoring='f1',
        n_jobs=-1
    )

    # 3. Calculations
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    val_mean = np.mean(val_scores, axis=1)
    val_std = np.std(val_scores, axis=1)

    # 4. Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(train_sizes, train_mean, 'o-', color="red", label="Training Score")
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.1, color="red")
    
    plt.plot(train_sizes, val_mean, 'o-', color="green", label="Cross-Validation Score")
    plt.fill_between(train_sizes, val_mean - val_std, val_mean + val_std, alpha=0.1, color="green")

    plt.title("Learning Curves (Logistic Regression)")
    plt.xlabel("Training Set Size")
    plt.ylabel("F1-Score")
    plt.legend(loc="best")
    plt.grid(True)
    
    plt.savefig('learning_curve_plot.png')
    print("Success: Plot saved as 'learning_curve_plot.png'")
    plt.show()

if __name__ == "__main__":
    generate_learning_curve(X, y)