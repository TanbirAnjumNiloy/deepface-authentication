from django.shortcuts import render
from django.shortcuts import render, redirect
import base64
from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
import base64
from .models import FaceImage

# Create your views here.


def main (request):
    return render(request,'home/main.html ')


def datasetup(request):
    if request.method == 'POST':
        image_data_base64 = request.POST.get('image_data_base64')
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        address = request.POST.get('address')
        
        if image_data_base64:
            # Decode the base64 image data
            image_data_base64 = image_data_base64.split(',')[1]  # Remove data:image/jpeg;base64,
            image_data = base64.b64decode(image_data_base64)
            
            # Save the decoded image to the database
            image = ContentFile(image_data, name='myimage.jpg')  # Give a name to the image file
            FaceImage.objects.create(name=name, roll=roll, address=address, image=image)
            
    return render(request, 'home/datasetup.html')



import base64
import cv2
import numpy as np
import face_recognition
from django.shortcuts import render
from .models import FaceImage

def output(request):
    context = {}

    if request.method == 'POST':
        image_data_base64 = request.POST.get('image_data_base64')

        if image_data_base64:
            # base64 থেকে ছবি ডিকোড
            image_data = base64.b64decode(image_data_base64.split(',')[1])
            nparr = np.frombuffer(image_data, np.uint8)

            # OpenCV দিয়ে ইমেজ ডিকোড এবং BGR থেকে RGB কনভার্ট
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # ক্যাপচার করা ছবির ফেস এনকোডিং
            current_face_encodings = face_recognition.face_encodings(rgb_img)

            if len(current_face_encodings) > 0:
                all_faces = FaceImage.objects.all()
                for face in all_faces:
                    # ডাটাবেসের ছবি OpenCV দিয়ে লোড ও RGB কনভার্ট
                    stored_img = cv2.imread(face.image.path)
                    stored_rgb = cv2.cvtColor(stored_img, cv2.COLOR_BGR2RGB)
                    stored_face_encodings = face_recognition.face_encodings(stored_rgb)

                    if len(stored_face_encodings) > 0:
                        match = face_recognition.compare_faces(
                            [stored_face_encodings[0]],
                            current_face_encodings[0]
                        )
                        if match[0]:
                            context['matched_data'] = face
                            break
                else:
                    context['error'] = "There is no data available in database"
            else:
                context['error'] = "No face detected in the image"

    else:
        # GET রিকোয়েস্টে ডাটাবেসের সব ডাটা দেখানো (ক্যাপচার ছাড়াই)
        context['all_faces'] = FaceImage.objects.all()

    return render(request, 'home/output.html', context)



