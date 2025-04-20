import boto3
import os
import uuid

INPUT_FOLDERS = "./photos"
rekognition  = boto3.client('rekognition')
collection_id = 'clusters'

try:
    rekognition.create_collection(CollectionId=collection_id)
except rekognition.exceptions.ResourceAlreadyExistsException:
    pass


img_paths = [os.path.join(INPUT_FOLDERS, f) for f in os.listdir(INPUT_FOLDERS) 
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]

print(img_paths)


grouped_photos = {}
group_id_map = {}
no_face_group = []
group_counter = 0

for img_path in img_paths:
    with open(img_path, 'rb') as img_file:
        img_bytes = img_file.read()
    
    try:
        index_res = rekognition.index_faces(
            CollectionId=collection_id,
            Image={'Bytes': img_bytes},
            ExternalImageId=str(uuid.uuid4()),
            DetectionAttributes = [],
            MaxFaces=1,
            QualityFilter="AUTO"
        )


        if not index_res['FaceRecords']:
            no_face_group.append(img_path)
            continue
            
        face_id = index_res['FaceRecords'][0]['Face']['FaceId']

        search_res = rekognition.search_faces(
            CollectionId=collection_id,
            FaceId=face_id,
            FaceMatchThreshold=90,
            MaxFaces=1
        )


        if search_res['FaceMatches']:
            match_face_id = search_res['FaceMatches'][0]['Face']['FaceId']

            if match_face_id in group_id_map:
                group_id = group_id_map[match_face_id]
            else:
                group_id = f"group_{group_counter}"
                group_id_map[match_face_id] = group_id
                grouped_photos[group_id] = []
                group_counter += 1
            
        else:
            group_id = f"group_{group_counter}"
            group_id_map[face_id] = group_id
            grouped_photos[group_id] = []
            group_counter += 1
        
        grouped_photos[group_id].append(img_path)
    
    except Exception as e:
        print(f"Error processing the image {img_path}: {e}")
        no_face_group.append(img_path)

grouped_photos['no_face'] = no_face_group


for group, image in grouped_photos.items():
    print(f"\n {group}")
    for img in image:
        print(f" - {img}")








