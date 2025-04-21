from .models import Audio, FIR, PoliceOfficer
from .serializers import AudioSerializer, RegisterSerializer, LoginSerializer, PoliceOfficerSerializer
from django.conf import settings
import os
from .ai_services import audio_to_text, generate_fir
from .utils import generate_pdf
from dotenv import load_dotenv
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files import File


load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


@api_view(["POST"])
@permission_classes([AllowAny])
def register_police(request):
    """ Register a new police officer """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_police(request):
    """ Authenticate and return JWT token """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """ Get logged-in police officer's profile """
    officer = request.user
    serializer = PoliceOfficerSerializer(officer)
    return Response(serializer.data)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def upload_audio(request):
    """ Uploads an audio file and automatically converts it to text """
    context = {
        "request": request
    }
    serializer = AudioSerializer(data=request.data, context=context)

    if serializer.is_valid():
        audio_instance = serializer.save()

        # Convert Audio to Text Immediately After Upload
        raw_text = audio_to_text(audio_instance.audio_file.path)
        audio_instance.transcribed_text = raw_text  # Save transcribed text in DB
        audio_instance.save()

        return Response({
            "status": "success",
            "message": "Audio uploaded and converted to text",
            "data": {
                "audio_id": audio_instance.id,
                "audio_file": request.build_absolute_uri(audio_instance.audio_file.url),
                "transcribed_text": raw_text,
                "created_at": audio_instance.created_at
            }
        })

    return Response({"status": "error", "message": serializer.errors}, status=400)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def convert_audio_to_fir(request, audio_id):
    """ Generate FIR from stored audio transcription """
    try:
        audio = Audio.objects.get(id=audio_id)
    except Audio.DoesNotExist:
        return Response({"status": "error", "message": "Audio not found"}, status=404)

    # Ensure we have transcribed text
    if not audio.transcribed_text:
        return Response({"status": "error", "message": "Audio transcription missing"}, status=400)

    # Generate FIR text
    fir_text = generate_fir(audio.transcribed_text)

    # Create FIR Entry in DB
    fir_instance = FIR.objects.create(
        original_text=audio.transcribed_text,
        fir_text=fir_text,
        audio=audio
    )

    # Generate FIR PDF and store it properly
    pdf_path = generate_pdf(fir_instance)

    # Open the file as a Django File object
    with open(pdf_path, "rb") as pdf_file:
        fir_instance.fir_pdf.save(os.path.basename(
            pdf_path), File(pdf_file), save=True)

    return Response({
        "status": "success",
        "case_id": fir_instance.case_id,
        "audio_file": request.build_absolute_uri(audio.audio_file.url),
        "transcribed_text": audio.transcribed_text,
        "fir_text": fir_instance.fir_text,
        "created_at": fir_instance.created_at,
        "fir_pdf": request.build_absolute_uri(fir_instance.fir_pdf.url),
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def get_fir_details(request, case_id):
    """ Fetch FIR details using Case ID """
    try:
        fir = FIR.objects.get(case_id=case_id)
    except FIR.DoesNotExist:
        return Response({"status": "error", "message": "FIR not found"}, status=404)

    return Response({
        "status": "success",
        "case_id": fir.case_id,
        # Victim's voice
        "audio_file": request.build_absolute_uri(fir.audio.audio_file.url),
        "transcribed_text": fir.original_text,  # Raw text
        "fir_text": fir.fir_text,  # Raw FIR text
        "created_at": fir.created_at,  # Timestamp
        "fir_pdf": request.build_absolute_uri(fir.fir_pdf.name)  # PDF URL
    })
