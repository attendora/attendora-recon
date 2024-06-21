import os
import face_recognition

def checkFaces(reference_image_folder, test_faces_folder):

    # Load the reference image
    reference_file = os.listdir(reference_image_folder)[0]
    reference_image = face_recognition.load_image_file(os.path.join(reference_image_folder, reference_file))
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    # Iterate over the test faces
    distance_threshold = 0.5
    ignore_threshold = 0.7
    distances= []
    for filename in os.listdir(test_faces_folder):
        test_face_path = os.path.join(test_faces_folder, filename)
        test_face_image = face_recognition.load_image_file(test_face_path)
        if len(face_recognition.face_encodings(test_face_image)) == 0:
            continue
        test_face_encoding = face_recognition.face_encodings(test_face_image)[0]

        # Compare the test face encoding with the reference encoding
        results = face_recognition.face_distance([reference_encoding], test_face_encoding)
        if results[0] > ignore_threshold:
            continue
        distances.append(results[0])

    if len(distances) > 0:
        avg_distance = sum(distances) / len(distances)
        if avg_distance < distance_threshold:
            return True
        else:
            return False
    else:
        return False