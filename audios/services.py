from django.contrib import messages
from audios.dao import AudioDAO, AudioUserDAO
from audios.forms import AudioForm
from audios.models import Audio, UserAudio
from users.dao import UserDAO


class AudioService:

    @staticmethod
    def get_audio_for_user(username, search=None):
        user = UserDAO.get_user_by_username(username)
        if user is None:
            return None, "User does not exist"
        
        if search:
            audios = AudioDAO.search_audios(search)
            flag = "search"
        if not search:
            audios = AudioUserDAO.get_user_audios(user)
            flag = "not_search"
        return (audios, flag)

    @staticmethod
    def load_audio(request) -> tuple[bool|Audio, str]:
        form = AudioForm(request.POST, request.FILES)
        if not form.is_valid():
            return None, "Form is invalid"#messages.warning(request, "Form is invalid")

        title = form.cleaned_data.get("title")
        author = form.cleaned_data.get("author")
        audio_file = form.cleaned_data.get("audio_file")
        if audio_file.size > 15 * 2**20:
            return None, "Your audio file is too big"
        if audio_file.name.endswith(".mp3"):
            audio = AudioDAO.create_audio(title, author,audio_file)
            return audio, "Audio uploaded successfully"
        else:
            return None, "Please upload an MP3 file"
        
    

class UserAudioService:

    @staticmethod
    def add_audio_for_user(request) -> str:
        audio_id = request.POST.get("audioId")
        audio = AudioDAO.get_audio(audio_id)
        if audio:
            if AudioUserDAO.is_exists_audio(request.user, audio):
                return "You already added this track"
            else:
                AudioUserDAO.create_user_audio(audio=audio, user=request.user)
                return "You successfuly add this track"
        else:
            return "Unknown error"

    @staticmethod
    def delete_audio_for_user(request) -> str:
        try:
            audio_id = request.POST.get("audioId")
            AudioUserDAO.delete_audio(request.user, audio_id)
            return "You delete this track successfully"
        except ValueError:
            return "Invalid ID"
        except Audio.DoesNotExist:
            return "Audio not found"
        except UserAudio.DoesNotExist:
            return "Track not found in your list"
        except Exception as e:
            return f"Unexpected error: {e}"
            



