# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 12:54:55 2020

@author: George
"""

import tkinter as tk
import random as rn
from PIL import Image, ImageTk
import speech_recognition as sr
from tkinter import messagebox
import re
from collections import namedtuple
import itertools
import os

import date.date_funcs as date_funcs
import internet.internet_funcs as internet_funcs
import translatorpack.translator as translator
import database.db_funcs as db_funcs


# Fonts
SMALLEST_FONT = ("Bahnschrift SemiLight", 8, 'bold')
SMALL_FONT = ("Bahnschrift SemiLight", 12, 'bold')
LARGE_FONT = ("Bahnschrift SemiLight", 16, 'bold')
CHINESE_FONT = ("DejaVu Sans Light", 20)

# Regex for validating dictionary entries
new_reg = '([\u4e00-\u9fff]{1,4}) \| ([a-z]{1,7}\d(?: [a-z]{1,7}\d?)*) \| ([\(\)\w]+(?: \w*)*(?:\/\w+(?: \w*)*)*)'

# Named tuple for storing words
TranslatedWord = namedtuple('TranslatedWord', 'character pinyin meaning')

# Layout management
num_rows = 8
num_cols = 4
row_min = 80


class Frame:
    bg = '#94212A'


class Header:
    width = 38
    height = 3
    bg = '#D8C3A5'
    fg = '#6D1A09'
    pad_x = 100
    pad_y = 30
    bd = 3
    relief = 'flat'


class QuestionLabel(Header):
    bg = '#94212A'
    fg = '#D8C3A5'
    width = 32


class SmallLabel(Header):
    height = 1
    bg = '#94212A'
    fg = '#D8C3A5'
    pad_y = 15


class LongTextLabel(SmallLabel):
    height = 20
    width = 68
    ipad_x = 10
    ipad_y = 10


class TallLabel(Header):
    bg = '#94212A'
    fg = '#D8C3A5'
    height = 2


class Entry:
    width = 60
    height = 11
    pad_y = 20


class SmallEntry(Entry):
    pad_y = 20
    ipad_y = 15


class Button:
    width = 15
    height = 1
    bg = '#D8C3A5'
    fg = '#6D1A09'
    pad_x = 0
    pad_y = 10


class BigButton(Button):
    pad_y = 20


class TestButton(Button):
    width = 12


class TopButton(Button):
    width = 5
    pad_x = 20
    pad_y = 20


class ImageP:
    height = 10
    width = 30


# Maps character options to database columns
map_char_set = {'Simplified': 'simp', 'Traditional': 'trad'}


class ChineseApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "HanLearn")

        container = tk.Frame(self)
        container.grid(sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (OpenPage, ExpPage, StartPage, ShowDictPage, BuildDictPage, AddingPage, TestPage, SettingsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)

        self.show_frame(OpenPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")


class OpenPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        labelhead = tk.Label(self, text="Welcome to HanLearn.", font=LARGE_FONT, bg=Header.bg,
                             bd=Header.bd, relief=Header.relief, fg=Header.fg)
        labelhead.grid(row=1, columnspan=3, padx=Header.pad_x, pady=Header.pad_y)
        labelhead.config(height=Header.height, width=Header.width)

        if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
            img_path = os.getcwd() + "\\chinese_repo\\images\\chinesewriting2.jpg"
        else:
            img_path = "images\\chinesewriting2.jpg"

        load = Image.open(img_path)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=2, column=1, rowspan=3, sticky='nsew')
        img.config(height=ImageP.height, width=ImageP.width)

        exp_button = tk.Button(self, text='How it works', font=SMALL_FONT,
                               command=lambda: controller.show_frame(ExpPage))
        exp_button.grid(row=5, column=1, pady=BigButton.pad_y, sticky='n')
        exp_button.config(height=BigButton.height, width=BigButton.width, bg=BigButton.bg, fg=BigButton.fg)

        proceed_button = tk.Button(self, text='Proceed', font=SMALL_FONT,
                                   command=lambda: controller.show_frame(StartPage))
        proceed_button.grid(row=6, column=1, pady=BigButton.pad_y, sticky='n')
        proceed_button.config(height=BigButton.height, width=BigButton.width, bg=BigButton.bg, fg=BigButton.fg)


class ExpPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT, command=lambda: controller.show_frame(OpenPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        labelhead = tk.Label(self, text="HanLearn", font=LARGE_FONT, bg=Header.bg, bd=Header.bd,
                             relief=Header.relief, fg=Header.fg)
        labelhead.grid(row=1, columnspan=4, padx=Header.pad_x, pady=Header.pad_y)
        labelhead.config(height=Header.height, width=Header.width)

        label = tk.Label(self, text=('''
                             
        
        HanLearn will randomly select a set of Chinese words from your word bank. It will then randomly display either the character, pinyin or meaning of that word and ask you to write either of the two remaining categories. 
        
        If you are correct, the game will move onto another word until all permutations of each word have been exhausted. 
        
        Once you feel that the word is sufficiently drilled into your brain hit 'Eliminate'. This will send the word to a separate bank, and you won't be tested on it for a week. When the amount of words in the second bank exceeds the number of entries required for testing (adjustable in settings), you will be retested on words in this bank. Follow the same process, and you will again be retested in one month so as to maximise vocabulary retention. 
        
        If the pinyin is selected as the question category, you can choose to have this read out loud instead of written. Equally, if pinyin is selected as the answer category, you may prefer to submit your answer by speech recognition.
  
        
                             '''),
                         font=SMALLEST_FONT, wraplength=500, bg=SmallLabel.bg, fg=SmallLabel.fg)
        label.grid(row=1, rowspan=5, columnspan=4, ipadx=LongTextLabel.ipad_x,
                   ipady=LongTextLabel.ipad_y)
        label.config(height=LongTextLabel.height, width=LongTextLabel.width)

        proceed_button = tk.Button(self, text='Proceed', font=SMALL_FONT,
                                   command=lambda: controller.show_frame(StartPage))
        proceed_button.grid(row=5, column=1, columnspan=2, pady=Button.pad_y)
        proceed_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        self.controller = controller

        if not db_funcs.check_for_table('user_words'):
            db_funcs.create_table('user_words')

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT, command=lambda: controller.show_frame(OpenPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        labelhead = tk.Label(self, text="HanLearn", font=LARGE_FONT, bg=Header.bg, bd=Header.bd,
                             relief=Header.relief, fg=Header.fg)
        labelhead.grid(row=1, columnspan=4, padx=Header.pad_x, pady=Header.pad_y)
        labelhead.config(height=Header.height, width=Header.width)

        checkd_button = tk.Button(self, text='Edit dictionary', font=SMALL_FONT,
                                  command=lambda: controller.show_frame(ShowDictPage))
        checkd_button.grid(row=3, column=1, columnspan=2, pady=Button.pad_y)
        checkd_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)

        buildd_button = tk.Button(self, text='Add to dictionary', font=SMALL_FONT,
                                  command=lambda: controller.show_frame(BuildDictPage))
        buildd_button.grid(row=4, column=1, columnspan=2, pady=Button.pad_y)
        buildd_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)

        self.test_button = tk.Button(self, text='Play Bank 1', font=SMALL_FONT,
                                     command=lambda: controller.show_frame(TestPage))
        self.test_button.grid(row=5, column=1, columnspan=2, pady=Button.pad_y)
        self.test_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)

        settings_button = tk.Button(self, text='Settings', font=SMALL_FONT,
                                    command=lambda: controller.show_frame(SettingsPage))
        settings_button.grid(row=6, column=1, columnspan=2, pady=Button.pad_y)
        settings_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)


class TestPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        self.controller = controller
        self.thing = 'yes'
        self.sound_button = None
        self.speak_button = None
        self.bank = 'bank1'

        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.result_var = tk.StringVar()
        self.ACs_display = tk.StringVar()  # initialise variable category string
        self.Qx_display = tk.StringVar()  # initialise variable question string

        back_button = tk.Button(self, text='Back', font=SMALL_FONT, command=lambda: controller.show_frame(StartPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        help_button = tk.Button(self, text='?', font=SMALL_FONT, command=self.show_help)
        help_button.grid(row=0, column=2, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='e')
        help_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        self.label1 = tk.Label(self, textvariable=self.ACs_display, font=LARGE_FONT, bg=Header.bg, fg=Header.fg)
        self.label1.grid(row=1, columnspan=3, padx=Header.pad_x, pady=Header.pad_y)
        self.label1.config(height=Header.height, width=Header.width)

        self.q_label = tk.Label(self, textvariable=self.Qx_display, font=CHINESE_FONT, bg=QuestionLabel.bg,
                                fg=QuestionLabel.fg)
        self.q_label.grid(row=2, rowspan=2, columnspan=3, pady=QuestionLabel.pad_y)
        self.q_label.config(height=QuestionLabel.height, width=QuestionLabel.width)

        self.q_label.bind("<Button-1>", self.hint)

        res_label = tk.Label(self, textvariable=self.result_var, font=SMALL_FONT, bg=SmallLabel.bg, fg=SmallLabel.fg)
        res_label.grid(row=4, columnspan=3, pady=SmallLabel.pad_y)

        self.entry = tk.Entry(self, font=SMALL_FONT, justify='center')
        self.entry.focus_set()
        self.entry.bind('<Return>', self.return_entry)
        self.entry.grid(row=5, columnspan=3, pady=SmallEntry.pad_y, ipady=SmallEntry.ipad_y)

        self.idk_button = tk.Button(self, text="I don't know", font=SMALL_FONT, command=self.idk)
        self.idk_button.grid(row=6, column=0, pady=TestButton.pad_y, sticky='e')
        self.idk_button.config(height=TestButton.height, width=TestButton.width, bg=TestButton.bg, fg=TestButton.fg)

        eliminate_button = tk.Button(self, text="Eliminate", font=SMALL_FONT, command=self.remove_char)
        eliminate_button.grid(row=6, column=2, pady=TestButton.pad_y, sticky='w')
        eliminate_button.config(height=TestButton.height, width=TestButton.width, bg=TestButton.bg, fg=TestButton.fg)

    def on_show_frame(self, _):

        self.entry.delete(0, 'end')
        self.choose_bank()
        self.create_megalist(self.bank)
        if self.num_qs > 0:
            self.create_testlist()
            self.set_perm_list()
            self.assign_qa()
            self.display_qa()
        else:
            messagebox.showinfo('Alert', "You don't have any entries yet!")

    def choose_bank(self):

        """Choose bank if enough entries meet time elapsed requirement"""

        self.num_qs = app.frames[SettingsPage].numq_var.get()

        self.week_val, self.month_val = db_funcs.ready_counts()

        if self.month_val > self.num_qs:
            self.bank = 3
        elif self.week_val > self.num_qs:
            self.bank = 2
        else:
            self.bank = 1

    def create_megalist(self, bank):

        """
        Look up vocabulary list from bank
        """
        char_set = map_char_set[app.frames[SettingsPage].char_set_var.get()]
        word_results = db_funcs.get_user_words(char_set=char_set, bank=bank)
        split_results = [(w[0], w[1], (w[2].split('/'))) for w in word_results]
        self.megalist = [TranslatedWord(*result) for result in split_results]

        self.num_qs = self.num_qs if len(self.megalist) > self.num_qs else len(self.megalist)

    def create_testlist(self):

        """
        Selects values from megalist for testing
        """

        if self.bank == 1:
            self.meg_copy = self.megalist[:]

        # only consider values in bank added a week ago or longer
        elif self.bank == 2:
            self.meg_copy = []
            for tup in self.megalist:
                if date_funcs.date_checker(tup.date, 7):
                    self.meg_copy.append(tup)

        # only consider values in bank added a month ago or longer
        elif self.bank == 3:
            self.meg_copy = []
            for tup in self.megalist:
                if date_funcs.date_checker(tup.date, 30):
                    self.meg_copy.append(tup)

        self.test_list = []

        # number of qs cannot exceed bank length
        self.num_qs = self.num_qs if len(self.meg_copy) > self.num_qs else len(self.meg_copy)

        for _ in range(self.num_qs):
            self.tup = rn.choice(self.meg_copy)
            self.test_list.append(self.tup)
            self.meg_copy.remove(self.tup)

    def set_perm_list(self):

        """
        Resets QA permutation list
        """

        nums = range(self.num_qs)
        qa_combinations = ['PM', 'PC', 'MC', 'MP']

        perm_list = itertools.product(nums, qa_combinations)
        perm_list = ((tup[0], tup[1][0], tup[1][1]) for tup in perm_list)

        PermTup = namedtuple('PermTup', 'index answer question')
        perm_tups = (PermTup(*tup) for tup in perm_list)
        self.perm_list = list(perm_tups)

    def assign_qa(self):

        """
        Selects question and answer pair
        """

        self.perm = rn.choice(self.perm_list)  # randomly select QA permutation

        # randomly select TranslatedWord tuple
        self.ran_tup = self.test_list[int(self.perm.index)]

        # randomly select answer category
        if self.perm.answer == 'C':
            self.Ax = self.ran_tup.character
            self.ACs = 'character'
        elif self.perm.answer == 'P':
            self.Ax = self.ran_tup.pinyin
            self.ACs = 'pinyin'
        elif self.perm.answer == 'M':
            self.Ax = self.ran_tup.meaning
            self.ACs = 'meaning'

        # randomly select question category
        if self.perm.question == 'C':
            self.Qx = self.ran_tup.character
            self.QCs = 'character'
        elif self.perm.question == 'P':
            self.Qx = self.ran_tup.pinyin
            self.QCs = 'pinyin'
        elif self.perm.question == 'M':
            self.Qx = self.ran_tup.meaning
            self.QCs = 'meaning'

    def display_qa(self):

        """
        Updates display with question and answer selection
        """

        if self.sound_button is not None:
            self.sound_button.grid_remove()

        if self.speak_button is not None:
            self.speak_button.grid_remove()

        # reset result variable
        self.result_var.set('')

        # set Q display
        if self.QCs == 'meaning':
            Qx_formatted = '/\n'.join(self.Qx)
            self.Qx_display.set(Qx_formatted)
        else:
            self.Qx_display.set(self.Qx)

        # set A category display
        self.ACs_display.set('Enter the %s for...' % self.ACs)

        # enable idk button
        self.idk_button.config(state='normal')

        self.speak_sound_buttons()

    def get_audio(self):

        """Captures voice and converts to pinyin"""

        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.record(source, duration=2)
            said = ''

            self.entry.delete(0, 'end')

            try:
                self.said = r.recognize_google(audio, language='zh-CN')
                self.said_pin = translator.chin_trans(self.said)[1]
            except:
                self.said_pin = ''

            self.entry.insert(0, self.said_pin)

        return said

    def speak_sound_buttons(self):

        """
        Places speak/sound buttons if activated in Settings
        and right category combination
        """

        if app.frames[SettingsPage].sound_var.get():
            if self.QCs == 'pinyin':
                self.Qx_display.set('')
                translator.speakit(self.ran_tup.character)
                self.sound_button = tk.Button(self, text='Play Again', font=SMALL_FONT,
                                              command=lambda: translator.speakit(self.ran_tup.character))
                self.sound_button.grid(row=2, rowspan=2, columnspan=4, pady=Button.pad_y)
                self.sound_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)

        if app.frames[SettingsPage].speak_var.get():
            if self.ACs == 'pinyin':
                self.speak_button = tk.Button(self, text='Speak', font=SMALL_FONT, command=self.get_audio)
                self.speak_button.grid(row=6, column=1)
                self.speak_button.config(height=Button.height, width=Button.width, bg=Button.bg, fg=Button.fg)

    def test(self, inp):

        """
        Evaluates user entry and displays result
        """

        if (self.ACs == 'pinyin' and inp.replace(' ', '') == self.Ax.replace(' ', '') or
                self.ACs == 'meaning' and inp in self.Ax):
            self.result = 'Correct'  # display if correct
            self.perm_list.remove(self.perm)  # remove QA permutation if correct
            if self.perm_list:  # if perm_list has not been exhausted
                self.assign_qa()  # generate new QA combination
            else:
                self.controller.show_frame(StartPage)

                # check tones
        elif self.ACs == 'pinyin':
            self.tone_checker(inp)

        else:
            self.result = 'Try again'  # display if incorrect

    def tone_checker(self, inp):

        """
        Checks to see if user entered correct sounds but incorrect tones
        """

        if ([i for i in inp.lower() if i.isalpha()] ==
                [i for i in self.Ax.lower() if i.isalpha()]):
            self.result = 'Incorrect tones'
        else:  # incorrect
            self.result = 'Try again'

    def idk(self):

        """
        Show answer if user cannot answer question
        """

        # delete text in entry field
        self.entry.delete(0, 'end')

        # display answer
        if self.ACs == 'meaning':
            Ax_formatted = '/ '.join(self.Ax)
        else:
            Ax_formatted = self.Ax
        self.result_var.set(f"Answer was '{Ax_formatted}'.")

        # disable button from being press
        self.idk_button.config(state='disabled')

        # keep permutation in list but reselect
        self.assign_qa()

        # wait one second then update QA display
        self.after(1000, self.display_qa)

    def return_entry(self, en):

        """
        Assigns text entry to input variable, tests if correct
        then updates result display string
        """

        self.inp = self.entry.get()

        # delete text in entry field
        self.entry.delete(0, 'end')

        # check user input
        self.test(self.inp)

        # display test result
        self.result_var.set(self.result)

        # wait one second, then choose new QA combination
        if self.result == 'Correct':
            self.after(1000, self.display_qa)

    def remove_char(self):

        """
        Removes character from current bank and sends to next
        """

        # remove TranslatedWord from megalist
        self.megalist.remove(self.ran_tup)

        # remove TranslatedWord from testlist
        self.test_list.remove(self.ran_tup)

        # removes one set of QA combinations from perm_list
        self.perm_list = self.perm_list[:-4]

        # update current bank with shortened megalist
        if self.bank == 3:
            db_funcs.remove_user_word(self.ran_tup.character)
        else:
            db_funcs.change_user_word_bank(self.ran_tup.character)

        if self.perm_list:
            self.assign_qa()
            self.display_qa()
        else:
            self.controller.show_frame[StartPage]

    def hint(self, event):

        """
        Generates a hint based on individual character meaning (requires internet connection)
        """

        chars = [i for i in self.Qx]

        message = ''

        if internet_funcs.internet_on():
            if self.QCs == 'character' and self.ACs == 'meaning':
                means = [translator.chin_trans(i)[2] for i in chars]
                for i in range(len(chars)):
                    message = message + (chars[i] + ' - ' + means[i].lower() + '\n')

        else:
            message = 'No internet connection'

        if message:
            messagebox.showinfo('Hint', message)

    def show_help(self):

        """Displays explanation of current page"""

        message = '''
        
        Try to answer the question and hit Enter once you have typed the answer
        
        If are stuck on the meaning of characters, clicking the Chinese word will reveal a clue (requires internet connection)
        
        If you cannot answer the question, press 'I don't know' to display the current answer and choose a new question
        
        Once you are certain that you know a word, press eliminate to send it to the next bank
        
        
                    '''
        messagebox.showinfo('Help', message)


class ShowDictPage(tk.Frame):

    def on_show_frame(self, _):
        self.temp_bank_contents = {}
        self.rw_data()

    def rw_data(self, bank=1):

        """
        Reads entries from the bank and displays in text box
        """

        self.bank_showing = bank
        if self.T.get("1.0", 'end-1c'):
            self.T.delete('1.0', 'end')

        if self.temp_bank_contents.get(bank, None) is None:
            char_set = map_char_set[app.frames[SettingsPage].char_set_var.get()]
            display_list = [TranslatedWord(*result) for result in db_funcs.get_user_words(char_set=char_set, bank=bank)]
        else:
            display_list = self.temp_bank_contents[bank]

        count = len(display_list)

        for tup in display_list:
            meaning = '/'.join(tup.meaning) if isinstance(tup.meaning, tuple) else tup.meaning
            vals = tup.character, tup.pinyin, meaning
            self.T.insert(tk.END, (' | '.join(vals) + '\n'))

        self.num.set('Number of entries: %d' % count)

    def text_to_list(self, list):

        """Reads entries from text box and adds word objects to list"""

        lineRegex = re.compile(new_reg)

        block = self.T.get("1.0", 'end-1c')
        lines = block.split('\n')
        lines = [line.strip() for line in lines if line]

        # check that entries have valid format
        state = True

        for line in lines:
            if not lineRegex.match(line):
                message = 'Line %d has an invalid format' % (lines.index(line) + 1)
                messagebox.showinfo('Error', message)
                state = False  # invalid line format found: do not update megalist

        # only perform if regex found no invalid entries
        if state:
            self.inp = self.T.get("1.0", 'end-1c')
            lines = self.inp.split('\n')
            for line in lines:
                if line:
                    mo = re.findall(lineRegex, line)[0]

                    char = mo[0]
                    pin = mo[1]
                    mean = mo[2]
                    mean = tuple(mean.split('/'))

                    translated_char = TranslatedWord(char, pin, mean)
                    list.append(translated_char)

    def switch_bank(self, from_bank, to_bank):

        """Switches display bank"""

        temp_megalist = []

        self.text_to_list(temp_megalist)

        self.temp_bank_contents[from_bank] = temp_megalist
        print(self.temp_bank_contents)

        self.rw_data(bank=to_bank)

    def write_bank(self, bank):

        """
        Updates bank with user entry
        """

        db_funcs.clear_table('user_words')

        current_bank_list = []
        self.text_to_list(current_bank_list)

        for key, value in self.temp_bank_contents.items():
            if key != self.bank_showing:
                for word in value:
                    db_funcs.add_to_user_word(word.character, bank=key)
            else:
                for word in current_bank_list:
                    db_funcs.add_to_user_word(word.character, bank=key)

        self.controller.show_frame(StartPage)

    def show_help(self):

        """Displays explanation of current page"""

        message = '''
        
        Here you can review and edit the entries that you will be tested on
        
        You will be tested on the second bank once it has enough entries that are over a week old
        
        The same goes for the third bank, with a period of one month instead
        
        
                    '''

        tk.messagebox.showinfo('Help', message)

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        self.controller = controller

        self.num = tk.StringVar()

        self.bind("<<ShowFrame>>", self.on_show_frame)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT,
                                command=lambda: self.controller.show_frame(StartPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        help_button = tk.Button(self, text='?', font=SMALL_FONT, command=self.show_help)
        help_button.grid(row=0, column=2, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='e')
        help_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        label1 = tk.Label(self, text='Your dictionary:', font=LARGE_FONT, bg=Header.bg, fg=Header.fg)
        label1.grid(row=1, columnspan=3, padx=Header.pad_x, pady=Header.pad_y)
        label1.config(height=Header.height, width=Header.width)

        button1 = tk.Button(self, text='1', font=SMALL_FONT,
                            command=lambda: self.switch_bank(from_bank=self.bank_showing, to_bank=1))
        button1.grid(row=2, column=0, columnspan=1, padx=Button.pad_x, pady=Button.pad_y, sticky='e')
        button1.config(bg=Button.bg, fg=Button.fg)

        button2 = tk.Button(self, text='2', font=SMALL_FONT,
                            command=lambda: self.switch_bank(from_bank=self.bank_showing, to_bank=2))
        button2.grid(row=2, column=1, columnspan=1, padx=Button.pad_x, pady=Button.pad_y)
        button2.config(bg=Button.bg, fg=Button.fg)

        button3 = tk.Button(self, text='3', font=SMALL_FONT,
                            command=lambda: self.switch_bank(from_bank=self.bank_showing, to_bank=3))
        button3.grid(row=2, column=2, columnspan=1, padx=Button.pad_x, pady=Button.pad_y, sticky='w')
        button3.config(bg=Button.bg, fg=Button.fg)

        char_count = tk.Label(self, textvariable=self.num, font=SMALL_FONT)
        char_count.grid(row=3, column=0, columnspan=3, padx=SmallLabel.pad_x, pady=SmallLabel.pad_y, sticky='n')
        char_count.config(bg=SmallLabel.bg, fg=SmallLabel.fg)

        self.T = tk.Text(self, height=Entry.height, width=Entry.width)
        self.T.grid(row=3, rowspan=3, columnspan=3)

        done_button = tk.Button(self, text='Done', font=SMALL_FONT,
                                command=lambda: (self.write_bank(self.bank_showing)))
        done_button.grid(row=6, column=1, pady=Button.pad_y)
        done_button.config(bg=Button.bg, fg=Button.fg)


class BuildDictPage(tk.Frame):

    def on_show_frame(self, event):

        self.addlist = []
        self.expvar.set('Enter Chinese words separated \nby a space, then hit enter.')

        if self.done_button is not None:
            self.done_button.grid_remove()

    def enter_chars(self, en):

        """Sends added words to next page"""

        self.inp1 = self.char_entry.get()
        self.char_entry.delete(0, 'end')

        chinRegex = re.compile('[^\u4e00-\u9fff\s]')

        if re.findall(chinRegex, self.inp1):
            messagebox.showinfo('Error', 'Enter only Chinese characters.')
        elif len(self.inp1) > 4 and ' ' not in self.inp1:
            messagebox.showinfo('Error', 'Enter spaces between words.')
        elif self.inp1 == '':
            messagebox.showinfo('Error', 'You have not entered any characters.')
        else:
            self.inp1 = list(self.inp1.split(' '))

            self.expvar.set("Continue adding words or click\n 'Next' to review entries.")

            self.done_button.grid(row=5, column=1, columnspan=2)
            self.done_button.config(bg=Button.bg, fg=Button.fg)

    def show_help(self):

        """Displays explanation of current page"""

        message = '''
        
        Here you can add new entries to the first bank
        
        Type individual Chinese words separated by a space, and then press Enter
        
        Repeat this as many times as you would like before pressing the Next button 
        
        On the next page you can review and edit the translations 
        
        
                    '''

        tk.messagebox.showinfo('Help', message)

    def translate_inp(self):

        """Obtains translations for entered words"""

        if internet_funcs.internet_on():
            error_message = ''
            for word in self.inp1:
                try:
                    self.addlist.append(db_funcs.search_by_char(word))
                except ValueError as ex:
                    error_message += (str(ex) + '\n')
            if error_message:
                messagebox.showinfo('Error', error_message)
            if self.addlist:
                self.controller.show_frame(AddingPage)
        else:
            messagebox.showinfo('Error',
                                'You need an internet connection to add to your bank')

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        self.controller = controller

        self.bind("<<ShowFrame>>", self.on_show_frame)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT, command=lambda: controller.show_frame(StartPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        help_button = tk.Button(self, text='?', font=SMALL_FONT, command=self.show_help)
        help_button.grid(row=0, column=2, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='e')
        help_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        head_label = tk.Label(self, text='Add words to dictionary', font=LARGE_FONT, bg=Header.bg, fg=Header.fg)
        head_label.grid(row=1, columnspan=4, padx=Header.pad_x, pady=Header.pad_y)
        head_label.config(height=Header.height, width=Header.width)

        self.expvar = tk.StringVar()

        exp_label = tk.Label(self, textvariable=self.expvar, font=SMALL_FONT, bg=TallLabel.bg, fg=TallLabel.fg)
        exp_label.grid(row=2, rowspan=2, columnspan=4, padx=TallLabel.pad_x, pady=TallLabel.pad_y)
        exp_label.config(height=TallLabel.height, width=TallLabel.width)

        self.char_entry = tk.Entry(self, font=SMALL_FONT, justify='center')
        self.char_entry.grid(row=4, columnspan=4, pady=Entry.pad_y)
        self.char_entry.bind('<Return>', self.enter_chars)

        self.done_button = tk.Button(self, text='Next', font=SMALL_FONT, command=self.translate_inp)


class AddingPage(tk.Frame):

    def write_data(self):

        """Display previously entered words with translation"""

        for tup in app.frames[BuildDictPage].addlist:
            add = (' | '.join(tup) + '\n')
            self.T.insert(tk.END, add)
        app.frames[BuildDictPage].addlist = []

    def on_show_frame(self, event):
        if self.T.get("1.0", 'end-1c'):
            self.T.delete('1.0', 'end')
        self.write_data()

    def write_bank(self):

        """Commit user entries to database"""

        self.megalist = []

        state = True

        lineRegex = re.compile(new_reg)

        block = self.inp = self.T.get("1.0", 'end-1c')
        lines = block.split('\n')
        lines = [line.strip() for line in lines if line]
        for line in lines:
            if not lineRegex.match(line):
                message = 'Line %d has an invalid format' % (lines.index(line) + 1)
                messagebox.showinfo('Error', message)
                state = False

        if state:

            self.inp = self.T.get("1.0", 'end-1c')
            lines = self.inp.split('\n')
            for line in lines:
                if line:
                    mo = re.findall(lineRegex, line)[0]

                    char = mo[0]
                    pin = mo[1]
                    mean = mo[2]
                    mean = tuple(mean.split('/'))

                    translated_char = TranslatedWord(char, pin, mean)

                    self.megalist.append(translated_char)

            for word in self.megalist:
                db_funcs.add_to_user_word(word.character)

            self.controller.show_frame(StartPage)

    def show_help(self):

        """Displays explanation of current page"""

        message = '''
        
        Verify that the translations are as expected and then press Done to add
        them to bank 1
        
        
                    '''

        tk.messagebox.showinfo('Help', message)

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        self.controller = controller

        self.bind("<<ShowFrame>>", self.on_show_frame)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT,
                                command=lambda: controller.show_frame(BuildDictPage))
        back_button.grid(row=0, column=0, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='w')
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        help_button = tk.Button(self, text='?', font=SMALL_FONT, command=self.show_help)
        help_button.grid(row=0, column=2, columnspan=2, padx=TopButton.pad_x, pady=TopButton.pad_y, sticky='e')
        help_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        label1 = tk.Label(self, text='Adding the following entries...', font=LARGE_FONT, bg=Header.bg,
                          fg=Header.fg)
        label1.grid(row=1, columnspan=4, padx=Header.pad_x, pady=Header.pad_y)
        label1.config(height=Header.height, width=Header.width)

        self.T = tk.Text(self, height=Entry.height, width=Entry.width)
        self.T.grid(row=2, rowspan=4, columnspan=4)

        done_button = tk.Button(self, text='Add', font=SMALL_FONT, command=self.write_bank)
        done_button.grid(row=6, column=1, columnspan=2, pady=Button.pad_y)
        done_button.config(bg=Button.bg, fg=Button.fg)


class SettingsPage(tk.Frame):

    def on_back(self):

        """Verifies question count input is valid"""

        if self.q_count.get().isdecimal():
            if int(self.q_count.get()) < 21:
                self.numq_var.set(self.q_count.get())
                self.controller.show_frame(StartPage)
            else:
                messagebox.showinfo('Error', 'Maximum number of characters is 20.')
        else:
            messagebox.showinfo('Error', 'Entry must be a number.')

    def on_show_frame(self, _):

        if internet_funcs.internet_on():
            self.sound_check.configure(state='active')
            self.speech_check.configure(state='active')
        else:
            self.sound_check.configure(state='disabled')
            self.speech_check.configure(state='disabled')

    def show_help(self):

        """Displays explanation of current page"""

        message = '''
        
        Here you can change the amount of characters that you will be tested on per round. This also sets the limit for amount of entries required to play banks 2 and 3
        
        The sound and speech options require an internet connection
        
        
                    '''

        tk.messagebox.showinfo('Help', message)

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent, bg=Frame.bg)

        for i in range(num_rows):
            self.rowconfigure(i, minsize=row_min, weight=1)

        for i in range(num_cols):
            self.columnconfigure(i, weight=1)

        self.controller = controller

        self.bind("<<ShowFrame>>", self.on_show_frame)

        back_button = tk.Button(self, text='Back', font=SMALL_FONT, command=self.on_back)
        back_button.grid(row=0, column=0, padx=TopButton.pad_x)
        back_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        help_button = tk.Button(self, text='?', font=SMALL_FONT, command=self.show_help)
        help_button.grid(row=0, column=3, padx=TopButton.pad_x)
        help_button.config(bg=TopButton.bg, fg=TopButton.fg, width=TopButton.width, height=TopButton.height)

        header = tk.Label(self, text='Settings', font=LARGE_FONT, bg=Header.bg, fg=Header.fg)
        header.grid(row=1, column=1, columnspan=2, pady=Header.pad_y)
        header.config(height=Header.height, width=Header.width)

        q_label = tk.Label(self, text='Number of characters per session: ', font=SMALL_FONT, bg=SmallLabel.bg,
                           fg=SmallLabel.fg)
        q_label.grid(row=2, column=1)
        q_label.config(height=SmallLabel.height, width=SmallLabel.width)

        self.numq_var = tk.IntVar()
        self.numq_var.set(10)

        self.q_count = tk.Entry(self, width=5)
        self.q_count.grid(row=2, column=2)
        self.q_count.insert(0, 10)

        self.sound_var = tk.IntVar()
        self.sound_var.set(0)

        self.sound_check = tk.Checkbutton(self, text='Enable sound', font=SMALL_FONT, bg=SmallLabel.bg,
                                          fg=SmallLabel.fg,
                                          onvalue=1, offvalue=0, variable=self.sound_var, selectcolor=SmallLabel.bg,
                                          activebackground=SmallLabel.bg, activeforeground=SmallLabel.fg)
        self.sound_check.grid(row=3, column=1)
        self.sound_check.config(height=SmallLabel.height, width=SmallLabel.width)

        self.speak_var = tk.IntVar()
        self.speak_var.set(0)

        self.speech_check = tk.Checkbutton(self, text='Enable speech recognition', font=SMALL_FONT, bg=SmallLabel.bg,
                                           fg=SmallLabel.fg, onvalue=1, offvalue=0, variable=self.speak_var,
                                           selectcolor=SmallLabel.bg, activebackground=SmallLabel.bg,
                                           activeforeground=SmallLabel.fg)
        self.speech_check.grid(row=4, column=1)
        self.speech_check.config(height=SmallLabel.height, width=SmallLabel.width)

        self.char_set_label = tk.Label(self, text='Choose character set', font=SMALL_FONT, bg=SmallLabel.bg,
                                       fg=SmallLabel.fg)
        self.char_set_label.grid(row=5, column=1)
        self.char_set_label.config(height=SmallLabel.height, width=SmallLabel.width)

        self.char_set_var = tk.StringVar()
        self.char_set_var.set('Simplified')

        self.char_set_option = tk.OptionMenu(self, self.char_set_var, 'Simplified', 'Traditional')
        self.char_set_option.grid(row=5, column=2)


app = ChineseApp()

if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
    icon_path = os.getcwd() + "\\chinese_repo\\images\\hl.ico"
else:
    icon_path = "images\\hl.ico"

app.iconbitmap(icon_path)

width = int(app.winfo_screenwidth() / 2)
height = int(app.winfo_screenheight() / 1.2)
w = app.winfo_reqwidth()
h = app.winfo_reqheight()

x = int(width - 2 * w)
y = int(height / 3) - h

app.geometry(f'{width}x{height}+{x}+{y}')
app.mainloop()
