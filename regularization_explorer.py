import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- Task 1: Data Preparation ---
def prepare_data(filepath="data/telecom_churn.csv"):
    df = pd.read_csv(filepath, index_col=0)
    df_processed = pd.get_dummies(df, drop_first=True)
    
    target = 'churned'
    X = df_processed.drop(columns=[target])
    y = df_processed[target]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, X.columns

# --- Task 2: Generate Coefficient Paths ---
def get_coef_paths(X, y, penalty, C_values):
    coef_list = []
    solver = 'liblinear' if penalty == 'l1' else 'l2' # Matches requirement
    
    for c in C_values:
        model = LogisticRegression(penalty=penalty, C=c, solver='liblinear')
        model.fit(X, y)
        coef_list.append(model.coef_[0])
        
    return np.array(coef_list)

# --- Task 3: Visualization ---
def plot_regularization_explorer(C_values, l1_paths, l2_paths, feature_names):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12), sharex=True)
    
    for i, feat in enumerate(feature_names):
        ax1.plot(C_values, l1_paths[:, i], label=feat)
        ax2.plot(C_values, l2_paths[:, i])

    ax1.set_xscale('log')
    ax1.set_title('L1 Regularization Path (Lasso)')
    ax1.set_ylabel('Coefficients')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='x-small')
    ax1.grid(True, alpha=0.3)

    ax2.set_xscale('log')
    ax2.set_title('L2 Regularization Path (Ridge)')
    ax2.set_ylabel('Coefficients')
    ax2.set_xlabel('C (Inverse Strength)')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('regularization_plot.png')
    plt.show()

if __name__ == "__main__":
    X_scaled, y, features = prepare_data()
    C_values = np.logspace(-3, 2, 20)
    
    print("Extracting L1 and L2 paths...")
    l1_paths = get_coef_paths(X_scaled, y, 'l1', C_values)
    l2_paths = get_coef_paths(X_scaled, y, 'l2', C_values)
    
    plot_regularization_explorer(C_values, l1_paths, l2_paths, features)
    print("Explorer complete. Plot saved.")