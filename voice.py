# For fun: python -m speech_recognition
from pynput.mouse import Button, Controller
import time
import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response



if __name__ == "__main__":

    NEXT = ["next", "next page", "flip", "flip page", "go to the next page", "okay"]
    BACK = ["previous", "previous page", "go back", "back", "go to the previous page"]
    DOWN = ["scroll down", "down", "go down", "scroll", "scroll down some more", "keep scrolling"]
    UP = ["scroll up", "up", "go up"]
    QUIT = ["quit", "end", "the end", "end program", "get me out", "get me out of here", "stop it", "please stop", "stop already", "escape", "stop"]

    PROMPT_LIMIT = 10

    mouse = Controller()

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
#    microphone = sr.Microphone(device_index=2)

    instructions = (
        "Welcome to voiced manga reader\n"
        "Voice commands included are:\n"
        "{nextCmd}\n"
        "{downCmd}\n"
        "{quitCmd}\n"
    ).format(nextCmd=', '.join(NEXT),
            downCmd=', '.join(DOWN),
            quitCmd=', '.join(QUIT))

    print(instructions)
    time.sleep(3)

    while 1:
        for j in range(PROMPT_LIMIT):
            print('Give me your command')
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if error found, end the program
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # mouse.position(800,500)
        if guess["transcription"].lower() in DOWN:
            print("down")
            mouse.scroll(0, -800)
        if guess["transcription"].lower() in UP:
            print("up")
            mouse.scroll(0, 800)
        elif guess["transcription"].lower() in NEXT:
            print("next page")
            mouse.click(Button.left, 1)
        elif guess["transcription"].lower() in BACK:
            print("prev page")
            mouse.click(Button.right, 1)
        elif guess["transcription"].lower() in QUIT:
            print("quit")
            break
