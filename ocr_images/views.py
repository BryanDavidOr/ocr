import sys

from django.shortcuts import render
import pytesseract
from .forms import ImageUpload
import os
from PIL import Image
from django.conf import settings
from rest_framework.views import APIView
import re
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from rest_framework.response import Response
from .serializer import *


class ReactView(APIView):
    serializer_class = ReactSerializer

    def get(self, request):
        text = ""
        numero_cedula = ""
        message = ""
        try:
            path = settings.MEDIA_ROOT
            camara = cv2.VideoCapture('rtsp://admin:asd12345@192.168.0.154:554/Streaming/Channels/102')
            return_value, imagen = camara.read()
            imagen = cv2.resize(imagen, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            # imagen = cv2.adaptiveThreshold(cv2.medianBlur(imagen, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            cv2.imwrite(path + "\images\\" + "captura1" + ".png", imagen)
            pathz = path + "\images\\" + "captura1" + ".png"
            pytesseract.pytesseract.tesseract_cmd = r'D:\Documentos\tesseract.exe'
            text = pytesseract.image_to_string(Image.open(pathz))
            # text = text.encode()
            # text = text.decode()

            summarized_text = re.findall(r'\d{9}-\d{1}', text)
            if summarized_text:
                summarized_text = summarized_text[0]
                summarized_text = summarized_text.replace("-", "")
                cedula = verificar(summarized_text)
                if cedula:
                    numero_cedula = summarized_text
            else:
                summarized_text = re.findall(r'\d{10}', text)
                if summarized_text:
                    summarized_text = summarized_text[0]
                    cedula = verificar(summarized_text)
                    if cedula is True:
                        numero_cedula = summarized_text
                else:
                    summarized_text = re.findall(r'\d{11}', text)
                    if summarized_text:
                        summarized_text = summarized_text[0]
                        summarized_text = summarized_text[1:]
                        cedula = verificar(summarized_text)
                        if cedula is True:
                            numero_cedula = summarized_text
                    else:
                        numero_cedula = "No se pudo reconocer ninguna cédula"
            os.remove(pathz)
        except:
            message = "asegurate de ingresar una imagen correcta"

        context = {
            'total_text': text,
            'summarized_text': numero_cedula,
            'message': message
        }

        """detail = [{"cedula": detail.cedula}
        for detail in Ocr.objects.all()]"""
        return Response(context)


# Create your views here.
def index(request):
    text = ""
    numero_cedula = ""
    message = ""
    if 'imagen' in request.POST:
        try:
            path = settings.MEDIA_ROOT
            camara = cv2.VideoCapture('rtsp://admin:asd12345@192.168.0.154:554/Streaming/Channels/102')
            return_value, imagen = camara.read()
            imagen = cv2.resize(imagen, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            # imagen = cv2.adaptiveThreshold(cv2.medianBlur(imagen, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
            cv2.imwrite(path + "\images\\" + "captura1" + ".png", imagen)
            pathz = path + "\images\\" + "captura1" + ".png"
            pytesseract.pytesseract.tesseract_cmd = r'D:\Documentos\tesseract.exe'
            text = pytesseract.image_to_string(Image.open(pathz))
            # text = text.encode()
            # text = text.decode()

            summarized_text = re.findall(r'\d{9}-\d{1}', text)
            if summarized_text:
                summarized_text = summarized_text[0]
                summarized_text = summarized_text.replace("-", "")
                cedula = verificar(summarized_text)
                if cedula:
                    numero_cedula = summarized_text
            else:
                summarized_text = re.findall(r'\d{10}', text)
                if summarized_text:
                    summarized_text = summarized_text[0]
                    cedula = verificar(summarized_text)
                    if cedula is True:
                        numero_cedula = summarized_text
                else:
                    summarized_text = re.findall(r'\d{11}', text)
                    if summarized_text:
                        summarized_text = summarized_text[0]
                        summarized_text = summarized_text[1:]
                        cedula = verificar(summarized_text)
                        if cedula is True:
                            numero_cedula = summarized_text
                    else:
                        numero_cedula = "No se pudo reconocer ninguna cédula"
            os.remove(pathz)
        except:
            message = "asegurate de ingresar una imagen correcta"

    elif 'archivo' in request.POST:
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                image = request.FILES['image']
                image = image.name
                path = settings.MEDIA_ROOT
                pathz = path + "/images/" + image
                pytesseract.pytesseract.tesseract_cmd = r'D:\Documentos\tesseract.exe'
                image = cv2.imread(pathz)
                image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # cv2.imwrite(path + "\images\\" + "captura2" + ".png", imagen)
                text = pytesseract.image_to_string(image)
                summarized_text = re.findall(r'\d{9}-\d{1}', text)
                if summarized_text:
                    summarized_text = summarized_text[0]
                    summarized_text = summarized_text.replace("-", "")
                    cedula = verificar(summarized_text)
                    if cedula:
                        numero_cedula = summarized_text
                else:
                    summarized_text = re.findall(r'\d{11}', text)
                    if summarized_text:
                        summarized_text = summarized_text[0]
                        summarized_text = summarized_text[1:]
                        cedula = verificar(summarized_text)
                        numero_cedula = summarized_text
                        if cedula is True:
                            numero_cedula = summarized_text
                    else:
                        summarized_text = re.findall(r'\d{10}', text)
                        if summarized_text:
                            summarized_text = summarized_text[0]
                            cedula = verificar(summarized_text)
                            if cedula is True:
                                numero_cedula = summarized_text
                        else:
                            numero_cedula = "No se pudo reconocer ninguna cédula"
                os.remove(pathz)
            except:
                message = "asegurate de ingresar una imagen correcta"
    context = {
        'total_text': text,
        'summarized_text': numero_cedula,
        'message': message
    }
    return render(request, 'formpage.html', context)


def verificar(nro):
    l = len(nro)
    if l == 10 or l == 13:  # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 24:  # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6:  # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(nro, 0)
                elif l == 13:
                    return __validar_ced_ruc(nro, 0) and nro[
                                                         10:13] == '001'  # se verifica que los ultimos numeros sean 001
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro, 1) and nro[10:13] == '001'  # sociedades publicas
            elif tercer_dig == 9:  # si es ruc
                return __validar_ced_ruc(nro, 2) and nro[10:13] == '001'  # sociedades privadas
            else:
                return False
        else:
            return False
    else:
        return False


def __validar_ced_ruc(nro, tipo):
    total = 0
    if tipo == 0:  # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])  # digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1:  # r.u.c. publicos
        base = 11
        d_ver = int(nro[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2)
    elif tipo == 2:  # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(nro[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0, len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
        else:
            total += p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture('rtsp://admin:asd12345@192.168.0.154:554/Streaming/Channels/102')

        (self.grabbed, self.frame) = self.video.read()
        return_value, image = self.video.read()
        cv2.imwrite('opencv' + '.png', image)
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass
