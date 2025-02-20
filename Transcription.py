# +=====================================================================+
# | ____    _    ____  _   _  ____    _    ____  _   _ _______        __|
# || __ )  / \  / ___|| | | |/ ___|  / \  / ___|| | | | ____\ \      / /|
# ||  _ \ / _ \ \___ \| |_| | |     / _ \ \___ \| |_| |  _|  \ \ /\ / / |
# || |_) / ___ \ ___) |  _  | |___ / ___ \ ___) |  _  | |___  \ V  V /  |
# ||____/_/   \_\____/|_| |_|\____/_/   \_\____/|_| |_|_____|  \_/\_/   |
# +=====================================================================+

#########################################################################
# // PYTHON ENVIRONMENT #################################################
# /usr/local/bin/python3 ################################################
# python:3.12 ###########################################################
# bashcashew (TLC) ######################################################
#########################################################################



#' ---------------------------------------------------------------
#' PACKAGES SECTION :D pipi install if needed...
import whisper
from pydub import AudioSegment
#' from pydub.silence import split_on_silence #' USED FOR OLDER SCRIPT VERSION, NOT NEEDED... BUT CAN BE USED.
import re
from tkinter import Tk, filedialog, messagebox
import sys
from datetime import timedelta
import textwrap
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' This is designed for adding a custom dictionary - can be used to replace "beta" with "𝛽"
custom_dictionary = {
    "and kneeling": "annealing",
    "simula ted": "simulated",
    "humb le": "humble",
    "polmadoro": "Pomodoro"
}
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' .wav is needded for for usage 
def convert_to_wav(input_file, output_file="converted_audio.wav"):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")
    return output_file
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Split audio into smaller chunks (needed for whisper's 30-60s formatting)
def split_audio_into_chunks(audio_file, chunk_length_ms=60000):
    audio = AudioSegment.from_file(audio_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Should manke a progress bar for the project completion 
