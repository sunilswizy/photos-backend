# import os
# import shutil
# from tqdm import tqdm
# import numpy as np
# import cv2
# from deepface import DeepFace
# from sklearn.cluster import DBSCAN

# INPUT_FOLDER = './photos'
# OUTPUT_FOLDER = 'grouped_photos'

# if not os.path.exists(OUTPUT_FOLDER):
#     os.makedirs(OUTPUT_FOLDER)

# img_paths = [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER)
#              if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]

# embeddings = []
# face_images = []
# original_paths = []

# print("Extracting faces...")

# for img_path in tqdm(img_paths):
#     try:
#         faces = DeepFace.extract_faces(img_path, detector_backend='opencv', align=True)

#         for face in faces:
#             embedding = DeepFace.represent(face['face'], model_name='Facenet', enforce_detection=False)

#             if isinstance(embedding, list) and len(embedding) > 0 and isinstance(embedding[0], dict):
#                 embeddings.append(embedding[0]['embedding'])
#                 face_images.append(face['face'])
#                 original_paths.append(img_path)

#     except Exception as e:
#         print(f"Error processing {img_path}: {e}")

# if not embeddings:
#     print("No faces found.")
#     exit()

# # Cluster embeddings
# embeddings = np.array(embeddings)
# clustering = DBSCAN(eps=0.4, min_samples=1, metric="euclidean").fit(embeddings)
# labels = clustering.labels_

# # Save clustered face crops
# for idx, label in enumerate(labels):
#     if label == -1:
#         continue

#     cluster_folder = os.path.join(OUTPUT_FOLDER, f"person_{label}")
#     os.makedirs(cluster_folder, exist_ok=True)

#     face_img = cv2.cvtColor(face_images[idx], cv2.COLOR_RGB2BGR)
#     cv2.imwrite(os.path.join(cluster_folder, f"face_{idx}.jpg"), face_img)

# print("Clustering completed successfully.")
