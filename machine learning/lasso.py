from sklearn.model_selection import train_test_split
from merge_xlsx import merge_excel


folder_path = "../data/tmp"

X, y = merge_excel(folder_path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
