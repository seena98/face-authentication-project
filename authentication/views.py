import glob
from typing import List, Dict
import copy
import face_recognition
from PIL import Image
from django.shortcuts import render
import os
# Create your views here.
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUserEntity, ImageEntity
from authentication.serializers import UserImageSerializer
from face_recognition_login import settings


class SignupView(APIView):
    http_method_names = ['post']
    permission_classes = [
        permissions.AllowAny
    ]
    renderer_classes = [
        JSONRenderer,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")


        images = dict((request.data).lists())['image']
        images = tuple(images)
        b = copy.deepcopy(images)
        no_face_images = []
        accepted_images = []
        # accepted_indexes = []
        counter = -1
        for image_elem in images:
            try:
                counter+=1
                person_image = image_elem
                person_image_PIL_obj = Image.open(person_image)
                # save new image to directory
                person_image_PIL_obj.save(settings.STATIC_ROOT + person_image.name)
                unknown_face_img = face_recognition.load_image_file(settings.STATIC_ROOT + person_image.name)
                person_image_encoding = face_recognition.face_encodings(face_image=unknown_face_img)[0]
                print("accepted image is : ")
                print(person_image)
                accepted_images.append(b[counter])  # <<<<<<<<<
                # accepted_indexes.append(counter)
                os.remove(settings.STATIC_ROOT + person_image.name)

            except Exception as error:
                print(error)
                # ROOT_DIR = os.path.abspath(os.curdir)
                # os.remove(ROOT_DIR +'/'+ person_image.name)
                no_face_images.append(image_elem.name)
        
        print(no_face_images)
        if len(accepted_images) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST,data = no_face_images)

        custom_user_entity = CustomUserEntity.objects.create(**{
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        })
        custom_user_entity.save()
        for acc_index in accepted_images:
            print("again accepted imagee is ")
            print(acc_index)
            # acc_img = Image.open(images[acc_index])
            # acc_img.save(settings.STATIC_ROOT + images[acc_index].name)
            user_img_dict = {}
            user_img_dict['custom_user_entity'] = custom_user_entity.id
            user_img_dict['image'] = acc_index
            user_image_serializer = UserImageSerializer(data=user_img_dict)
            isValid = user_image_serializer.is_valid()
            if isValid:
                user_image_serializer.save()
            else:
                print(user_image_serializer.errors)
        return Response(status=status.HTTP_201_CREATED,data=no_face_images)


class LoginView(APIView):
    http_method_names = ['post']
    permission_classes = [
        permissions.AllowAny
    ]
    renderer_classes = [
        JSONRenderer,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            person_image = dict((request.data).lists())['image'][0]
            person_image_PIL_obj = Image.open(person_image)
            # save new image to directory
            person_image_PIL_obj.save(settings.STATIC_ROOT + person_image.name)
            image_list = [Image.open(item) for i in
                          [glob.glob('staticfiles/photo/*.%s' % ext) for ext in ["jpg", "jpeg", "gif", "png", "tga"]] for
                          item in i]
            all_loaded_user_images: List = [face_recognition.load_image_file(user_image.filename) for user_image in
                                            image_list]
            all_encoded_user_images: List = [face_recognition.face_encodings(face_image=user_image)[0] for user_image in
                                             all_loaded_user_images]
            unknown_face_img = face_recognition.load_image_file(settings.STATIC_ROOT + person_image.name)
            person_image_encoding = face_recognition.face_encodings(face_image=unknown_face_img)[0]

            compare_result = face_recognition.compare_faces(all_encoded_user_images, person_image_encoding)
            users_images_to_compare_faces_result: Dict = {
                image_list[i].filename: compare_result[i]
                for i in range(len(image_list))
            }

            for user_image, user_image_compare_result in users_images_to_compare_faces_result.items():
                if user_image_compare_result:
                    user_image_entity = ImageEntity.objects.get(image=user_image)
                    data = {
                        "first_name": user_image_entity.custom_user_entity.first_name,
                        "last_name": user_image_entity.custom_user_entity.last_name,
                        "email": user_image_entity.custom_user_entity.email,
                        "image": face_recognition.face_locations(unknown_face_img),
                    }
                    return Response(data=data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print("the input image face not detected so we have to abort it :)")
            return Response(status=status.HTTP_400_BAD_REQUEST,data="no face detected from input image, try again")


