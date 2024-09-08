import glob
import os
import platform
import subprocess
import threading
import time

import pygame

NODE_DIR = os.path.dirname(os.path.abspath(__file__))


def list_all_sounds():
    return sum(
        [
            glob.glob(os.path.join(NODE_DIR, "*.{}".format(file.strip())))
            for file in "mp3, wav, m4a,aiff".split(",")
        ],
        [],
    )


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
any = AnyType("*")


class PassThroughWithSound:

    def __init__(self):
        pygame.mixer.init()

    @classmethod
    def INPUT_TYPES(cls):
        sound_files = list_all_sounds()
        sound_file_options = [os.path.basename(file) for file in sound_files]
        if not sound_file_options:
            sound_file_options = ["No sound files found"]

        return {
            "required": {
                "input": (any,),
                "sound_file_path": (
                    sound_file_options,
                    {"default": sound_file_options[0] if sound_file_options else ""},
                ),
                "show_alert": (["enable", "disable"], {"default": "enable"}),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = (any,)
    RETURN_NAMES = ("output",)
    FUNCTION = "execute"
    CATEGORY = "Custom"
    OUTPUT_NODE = True

    def show_alert(self, message):
        current_os = platform.system()

        if current_os == "Windows":
            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Add-Type -AssemblyName PresentationFramework; "
                    f"[System.Windows.MessageBox]::Show('{message}')"
                ]
            )
        elif current_os == "Darwin":  # macOS
            script = f'display alert "{message}"'
            subprocess.run(["osascript", "-e", script])
        elif current_os == "Linux":
            # Use zenity if available, otherwise fallback to notify-send
            try:
                subprocess.run(["zenity", "--info", "--text", message])
            except FileNotFoundError:
                subprocess.run(["notify-send", message])

    def play_sound(self, sound_file_path, show_alert):

        pygame.mixer.music.load(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), sound_file_path)
        )
        pygame.mixer.music.play(loops=1)

        # Wait until the sound finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def execute(self, input, sound_file_path, show_alert = "enable"):

        sound_thread = threading.Thread(
            target=self.play_sound, args=(sound_file_path, show_alert)
        )
        sound_thread.daemon = True  # Set the thread as a daemon thread
        sound_thread.start()
        if show_alert == "enable":
            self.show_alert("done!!")
        return (input,)

    def IS_CHANGED(s, input, sound_file_path, show_alert):
        # return str(input) + sound_file_path
        return ""

if __name__ == "__main__":
    message = "hi"
    subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Add-Type -AssemblyName PresentationFramework; "
                    f"[System.Windows.MessageBox]::Show('{message}')"
                ]
            )