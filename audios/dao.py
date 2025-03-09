from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

from users.models import Users
from .models import Audio, UserAudio

class AudioDAO:

    @staticmethod
    def search_audios(search: str):
        return Audio.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))

    @staticmethod
    def create_audio(title, author, audio_file):
        return Audio.objects.create(title=title, author=author, audio_file=audio_file)
 
    @staticmethod
    def get_audio(audio_id):
        return Audio.objects.get(id=audio_id)
    

class AudioUserDAO:

    @staticmethod
    def create_user_audio(user: Users, audio: Audio):
        return UserAudio.objects.create(audio=audio, user=user)
    
    @staticmethod
    def get_user_audios(user: Users):
        return UserAudio.objects.filter(user=user)
    
    @staticmethod
    @transaction.atomic
    def delete_audio(user: Users, audio_id: int):
        try:
            audio = Audio.objects.get(pk=audio_id)
            return UserAudio.objects.get(user=user, audio=audio).delete()
        except ObjectDoesNotExist:
            raise
    
    @staticmethod
    def is_exists_audio(user: Users, audio: Audio):
        return UserAudio.objects.filter(user=user, audio=audio).exists()
