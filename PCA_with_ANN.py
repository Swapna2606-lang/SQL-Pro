import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# -------------------------------
# LOAD DATASET
# -------------------------------
def load_images(path):
    if not os.path.exists(path):
        print("❌ Dataset folder not found:", path)
        exit()

    images = []
    labels = []
    label = 0

    for person in os.listdir(path):
        person_path = os.path.join(path, person)

        if os.path.isdir(person_path):
            for img_name in os.listdir(person_path):
                img_path = os.path.join(person_path, img_name)

                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                # Better resolution
                img = cv2.resize(img, (150, 150))

                images.append(img.flatten())
                labels.append(label)

            label += 1

    return np.array(images), np.array(labels)


# -------------------------------
# MAIN
# -------------------------------

# 🔥 FIXED FULL PATH (IMPORTANT)
dataset_path = r"C:\Users\rswap\OneDrive\Desktop\Faceproject\dataset"

print("📂 Loading dataset...")
X, y = load_images(dataset_path)

print("✅ Dataset Loaded")
print("Total Images:", len(X))

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)

# -------------------------------
# PCA
# -------------------------------
mean_face = np.mean(X_train, axis=0)

X_train_centered = X_train - mean_face
X_test_centered = X_test - mean_face

U, S, Vt = np.linalg.svd(X_train_centered, full_matrices=False)

# Improved k values
k_values = [20, 40, 60, 80, 100]
accuracies = []

for k in k_values:
    print(f"\n🔹 Processing k = {k}")

    eigenfaces = Vt[:k]

    X_train_pca = np.dot(X_train_centered, eigenfaces.T)
    X_test_pca = np.dot(X_test_centered, eigenfaces.T)

    # 🔥 Normalize data
    scaler = StandardScaler()
    X_train_pca = scaler.fit_transform(X_train_pca)
    X_test_pca = scaler.transform(X_test_pca)

    # 🔥 Improved ANN
    model = MLPClassifier(
        hidden_layer_sizes=(200, 100),
        max_iter=1000,
        random_state=42
    )

    model.fit(X_train_pca, y_train)

    y_pred = model.predict(X_test_pca)
    acc = accuracy_score(y_test, y_pred)

    accuracies.append(acc)
    print(f"✅ Accuracy for k={k}: {acc:.4f}")

# -------------------------------
# GRAPH
# -------------------------------
plt.plot(k_values, accuracies, marker='o')
plt.xlabel("k (Eigenfaces)")
plt.ylabel("Accuracy")
plt.title("Improved Accuracy vs k")
plt.grid()
plt.show()

print("\n🎉 PROJECT COMPLETED SUCCESSFULLY!")