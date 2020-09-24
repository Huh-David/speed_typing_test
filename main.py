import PySimpleGUI as sg
import urllib.request
import random
import time
import threading


def generate_random_string(random_words=[]):
    string = ""

    if not random_words:
        word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()

        random_words = long_txt.splitlines()

        for x in range(total_words):
            string += random.choice(random_words) + " "

        global total_chars
        total_chars = len(string)

    else:
        for x in range(len(random_words)):
            string += random_words[x] + " "

    return string


def calculate_time_since_start():
    while not won:
        if starting_time != 0:
            seconds = time.time() - starting_time
        else:
            seconds = 0

        string = "Seconds since start: " + str(round(seconds, 2))
        window.FindElement('_TIME_').Update(string)


def check_input(user_input, word):
    if user_input in word:
        if word.index(user_input) == 0:
            return True
    return False


def generate_ui():
    global won
    global starting_time
    global window
    global total_words
    global total_chars

    time_started = False
    won = False
    total_words = 10

    sg.theme("DarkAmber")

    random_word = generate_random_string()

    layout = [[sg.Text("Seconds since start: 0.00 ", key='_TIME_')],
              [sg.Text("You had " + str(total_words) + " words and " + str(total_chars) + " chars", visible=False,
                       key='_WIN_')],
              [sg.Text("Chars per min: 123123", visible=False,
                       key='_STATS_')],
              [sg.Text(random_word, key='_WORD_')],
              [sg.InputText(enable_events=True, key='_INPUT_')],
              [sg.Button("Ok")]]
    window = sg.Window(title="Speed Typing Test", layout=layout, margins=(100, 50))

    while True:
        event, values = window.read()

        if not time_started and len(values['_INPUT_']) != 0:
            time_started = True
            starting_time = time.time()
            thread = threading.Thread(target=calculate_time_since_start)
            thread.start()

        if check_input(values['_INPUT_'], random_word):  # everything is correct
            if values['_INPUT_'] + " " == random_word:
                won = True

                window.FindElement('_INPUT_').Update("")
                window.FindElement('_WORD_').Update(
                    "YOU HAVE WON IN " + str(round(time.time() - starting_time, 2)) + " seconds")
                window.FindElement('_WIN_').Update(visible=True)
                window.FindElement('_STATS_').Update(visible=True, value="Chars per min: " +
                                                                         str(round(60 * total_chars / (
                                                                                 time.time() - starting_time), 2)))

            if values['_INPUT_'] and values['_INPUT_'][-1] == " ":
                window.FindElement('_INPUT_').Update("")
                random_word = generate_random_string(random_word.split(" ")[1:-1])
                window.FindElement('_WORD_').Update(random_word)
            window.FindElement('_WORD_').Update(text_color='green')
        else:  # something is not correct
            window.FindElement('_WORD_').Update(text_color='red')

        if event == "Ok" or event == sg.WINDOW_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    generate_ui()
