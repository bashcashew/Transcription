# +=========================================================================+
# ||  ____    _    ____  _   _  ____    _    ____  _   _ _______        __ ||
# || | __ )  / \  / ___|| | | |/ ___|  / \  / ___|| | | | ____\ \      / / ||
# || |  _ \ / _ \ \___ \| |_| | |     / _ \ \___ \| |_| |  _|  \ \ /\ / /  ||
# || | |_) / ___ \ ___) |  _  | |___ / ___ \ ___) |  _  | |___  \ V  V /   ||
# || |____/_/   \_\____/|_| |_|\____/_/   \_\____/|_| |_|_____|  \_/\_/    ||
# +=========================================================================+

#############################################################################
# // PYTHON ENVIRONMENT #####################################################
# Tested on python:3.12 #####################################################
# bashcashew ################################################################
#############################################################################



#' ---------------------------------------------------------------
#' PACKAGES SECTION :D pipi install if needed...
import whisper
from pydub import AudioSegment
#' from pydub.silence import split_on_silence #' USED FOR OLDER SCRIPT VERSION, NOT NEEDED... BUT CAN BE USED.
import re #' used for the splits and dictionary splits
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
def audio_to_chunkies(audio_file, chunk_length_ms=60000):
    audio = AudioSegment.from_file(audio_file)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Should manke a progress bar for the project completion 
def progress_bar(percentage):
    bar_length = 50
    block = int(bar_length * percentage / 100)
    progress = f"\rProgress: [{'#' * block}{'.' * (bar_length - block)}] {percentage:.2f}%"
    sys.stdout.write(progress)
    sys.stdout.flush()
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Uses Whisper to transcribe on a per-chunk basis
def transcribe_audio_chunks(chunks):
    model = whisper.load_model("base")
    full_transcription = []
    timestamp = 0
    for i, chunk in enumerate(chunks):
        #' Chunk .wav sav for transcribing each partition
        chunk.export("temporarily_chunky.wav", format="wav")
        #' Loading the chunky and transcribing
        result = model.transcribe("temporarily_chunky.wav", fp16 = False) #' Gives error on arch.. fp32 is suuitable unless soft-error occurs with "False"
        sentences = re.split(r'(?<=[.!?]) +', result['text'])
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                time_str = str(timedelta(milliseconds=timestamp))[:-3]  #' HH:MM:SS.mmm --> should negate microseconds from occurring
                formatted_sentence = f"{time_str.ljust(12)} {sentence}"
                wrapped_sentence = textwrap.fill(formatted_sentence, width=80, subsequent_indent='               ')
                full_transcription.append(wrapped_sentence)
            timestamp += len(chunk) // len(sentences) if len(sentences) > 0 else 0
        #' Percentage increase when chunk is "solved"
        percentage = ((i + 1) / len(chunks)) * 100
        progress_bar(percentage)
    sys.stdout.write("\n")
    return '\n\n'.join(full_transcription)
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Dictonary override for the phrases and/or replacements needed
def custom_corrections(text):
    for incorrect, correct in custom_dictionary.items():
        text = re.sub(re.escape(incorrect), correct, text, flags=re.IGNORECASE)
    return text
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Function to select a file using a file dialog
def select_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select an Appropriate File", filetypes=[("Audio/Video files", "*.wav *.mp3 *.mp4 *.m4a *.flac *.avi *.mov *.mkv")])
    return file_path
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' Function to get output file name using a dialog
def get_output_file():
    root = Tk()
    root.withdraw()
    output_file = filedialog.asksaveasfilename(title="Save Transcription As", defaultextension=".md", filetypes=[("Text files", "*.md")])
    return output_file
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
#' MAIN FUNCTION
def process_audio_video():
    input_file = select_file()
    if not input_file:
        messagebox.showinfo("No File Selected", "Please select a valid audio or video file.")
        return
    output_file = get_output_file()
    if not output_file:
        messagebox.showinfo("No Output File", "Please provide a valid output file path.")
        return
    #' .wav conversion
    audio_file = convert_to_wav(input_file)
    print("Audio conversion successful!")
    #' Split to the chunkies
    chunks = audio_to_chunkies(audio_file)
    print(f"Audio split into {len(chunks)} chunks.")
    #' Transcribe
    raw_transcription = transcribe_audio_chunks(chunks)
    print("Transcription complete!\nNow correcting and formatting...")
    #' Apply custom corrections
    corrected_transcription = custom_corrections(raw_transcription)
    print("Transcription corrected and formatted.")
    #' Save to a text file
    with open(output_file, 'w') as f:
        f.write(corrected_transcription)
    print(f"Transcription saved to {output_file}")
    messagebox.showinfo("Transcription Complete! :D", f"Saved to {output_file}.")
#' ---------------------------------------------------------------



#' ---------------------------------------------------------------
if __name__ == "__main__":
    process_audio_video()
#' ---------------------------------------------------------------


