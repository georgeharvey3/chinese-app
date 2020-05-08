# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 18:20:14 2020

@author: George
"""

from googletrans import Translator
import pinyin as py
import unidecode
from gtts import gTTS
import pygame
import io


def chin_trans(char):
    """Translates character"""

    translator = Translator()
    m = (translator.translate(char, src='zh-CN', dest='en'))
    p = (translator.translate(char, src='zh-CN', dest='zh-CN'))
    pron = p.pronunciation

    if ' ' in pron:  # remove spaces from google pronunciation
        pron = pron.split(' ')
        pron = ''.join(pron)

    bad_pron = get_pyn(char)  # find python pronunciation
    new_pron = converter(pron, bad_pron)  # change google translation to numerical

    return char, new_pron, m.text.lower()


def get_pyn(chara):
    """Obtains pronunciation for character"""

    pin1 = py.get(chara, format='numerical')  # gets unreliable pinyin in numerical form

    ps1 = []

    for i in pin1[:-1]:  # removes numbers and separates string between words
        if i.isalpha():
            ps1.append(i)
        elif i.isnumeric():
            ps1.append(' ')

    pin_as = ''.join(ps1)  # creates string

    return pin_as


def umlaut_to_v(inp):
    """switches umlaut u to a v in pinyin"""

    inp_v = []
    for i in inp:
        if any((i == c for c in ('ü', 'ǜ', 'ǚ', 'ǘ', 'ū'))):
            inp_v.append('v')
        else:
            inp_v.append(i)
    inp = ''.join(inp_v)

    return inp


def unaccent(word):
    """Removes accent from pinyin"""

    word_un = unidecode.unidecode(word)

    word_un_lower = word_un.lower()

    return word_un_lower


def num_maker(wrd):
    """Converts accent into relative numerical tone"""

    one = ['ā', 'ē', 'ī', 'ō', 'ū']
    two = ['á', 'é', 'í', 'ó', 'ú', 'ǘ']
    three = ['ǎ', 'ě', 'ǐ', 'ǒ', 'ǔ', 'ǚ']
    four = ['à', 'è', 'ì', 'ò', 'ù', 'ǜ']

    if any((True for x in one if x in wrd)):
        num = '1'
    elif any((True for x in two if x in wrd)):
        num = '2'
    elif any((True for x in three if x in wrd)):
        num = '3'
    elif any((True for x in four if x in wrd)):
        num = '4'
    else:
        num = ''

    return num


def apply_num(wrds):
    """finds numerical tones"""

    nums = list(map(num_maker, wrds))

    return nums


def separator(a, b):
    """Separates pinyin sounds"""

    n2 = []

    off = 0

    for i in range(len(b)):  # finds offsets of spaces
        if b[i] == ' ':
            n2.append(i - off)
            off += 1

    a_new = []

    for i in range(len(a)):  # splits google translation up
        a_new.append(a[i])
        if i + 1 in n2:
            a_new.append(' ')

    a_fin = ''.join(a_new)
    a_fin = a_fin.split(' ')

    return a_fin


def converter(tr, py):
    """Converts from Google pinyin to accurate pinyin"""

    tr = separator(tr, py)  # split accurate pinyin
    ns = apply_num(tr)  # find numerical tone
    tr = list(map(umlaut_to_v, tr))
    tr = list(map(unaccent, tr))  # remove accent

    fin = []

    length = len(py.split(' '))

    for i in range(length):
        fin.append(tr[i] + ns[i])  # add numerical tone to word

    fin = ''.join(fin)  # create string

    return fin


def speakit(text):
    """Reads pinyin aloud"""

    tts = gTTS(text, lang='zh-CN', slow=False)
    pygame.mixer.init()
    pygame.init()
    with io.BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)
        pygame.mixer.music.load(f)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        pygame.mixer.music.play()
        pygame.event.wait()
