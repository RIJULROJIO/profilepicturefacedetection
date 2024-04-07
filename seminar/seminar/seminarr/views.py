import base64
from django.shortcuts import render
from django.contrib import messages
# from .utils import *
from django.views.generic import View

# Create your views here.



# In your views.py file

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Assuming you have a template named 'home.html'



import cv2
import numpy as np


from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage

# Your existing code...

# Update your view function
from django.core.files.base import ContentFile

# Your other imports...



def upload_profile_picture(request):
    if request.method == "POST":
        photo_id = request.FILES.get('photoid')
        camera_photo = request.POST.get('camera_photo')

        try:
            if photo_id:
                # If a photo is uploaded
                validate_image(photo_id)
                messages.success(request, "Face detection successful. Profile picture uploaded.")

                # Store the image temporarily
                fs = FileSystemStorage()
                filename = fs.save(photo_id.name, photo_id)
                uploaded_file_url = fs.url(filename)

            elif camera_photo:
                # If a photo is captured
                decoded_photo = np.frombuffer(base64.b64decode(camera_photo.split(',')[1]), dtype=np.uint8)
                validate_image(decoded_photo)
                messages.success(request, "Face detection successful. Profile picture captured.")

                # Create a ContentFile from the bytes
                content_file = ContentFile(decoded_photo.tobytes(), name='captured_photo.jpg')

                # Store the image temporarily (adjust as needed)
                fs = FileSystemStorage()
                captured_photo_url = fs.save(content_file.name, content_file)

                # Pass the captured photo URL to the template
                return render(request, 'check_face_detection.html', {'captured_photo_url': fs.url(captured_photo_url)})

            else:
                raise ValidationError("Please upload a valid image file or capture a photo.")

            # Pass the uploaded file URL to the template
            return render(request, 'check_face_detection.html', {'uploaded_file_url': uploaded_file_url})

        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect('upload_profile_picture')

    return render(request, 'upload_profile_picture.html')


from mtcnn import MTCNN

def validate_image(photo_id):
    if isinstance(photo_id, np.ndarray):
        # Case when a photo is captured
        img = cv2.cvtColor(photo_id, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    elif hasattr(photo_id, 'read'):
        # Case when a file is uploaded
        img = cv2.imdecode(np.frombuffer(photo_id.read(), np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    else:
        raise ValidationError("Invalid image format.")

    # Use MTCNN for face detection
    detector = MTCNN()
    faces = detector.detect_faces(img)

    # Filter out non-human faces
    human_faces = [face for face in faces if face['confidence'] > 0.95 and face['confidence'] <= 1.0]

    if len(human_faces) == 0:
        raise ValidationError("No human face detected in the uploaded image.")

    if len(human_faces) > 1:
        raise ValidationError("Multiple human faces detected. Please upload a photo with only one face.")

    # Check for blurriness
    if is_blurry(img):
        raise ValidationError("Image is blurry. Please upload a clear photo.")


def is_blurry(image, threshold=100):
    # Calculate the variance of Laplacian
    laplacian_var = cv2.Laplacian(image, cv2.CV_64F).var()
    return laplacian_var < threshold

# Your existing code...
def decode_base64(data):
    if data is None:
        return None

    img_data = base64.b64decode(data.split(',')[1])
    return np.frombuffer(img_data, dtype=np.uint8)

def check_face_detection(request):
    return render(request, 'check_face_detection.html')





from django.shortcuts import redirect
