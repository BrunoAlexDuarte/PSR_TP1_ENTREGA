import threading
import time
import readchar
import random

from pprint import pprint
from collections import namedtuple
from colorama import Fore, Back, Style


Input = namedtuple('Input', ['requested', 'received', 'duration'])
inputs = []
time_initial_str = 0
time_initial = 0
finished_event = None
max_time = 0

# Função para gerar letras aleatoriamente
def gera_letra():
    return chr(ord('a') + random.randint(0,25))

# Thread para bloquear o programa ao fim do tempo definido
def show_results_time():
    global finished_event
    #finished_event.wait(max_time)
    global max_time
    while(max_time > 0 and not finished_event.is_set()):
        time.sleep(1)
        max_time -= 1
    finished_event.set()
    show_results(" because the time is up")

# Apresentação das estatísticas do jogo
def show_results(add):
    global inputs
    print(Style.RESET_ALL + Back.RED + Fore.WHITE + "The test is over" + add + Style.RESET_ALL)
    my_dict = {}
    len_total = len(inputs)
    hits = []
    total_time = 0

    if(len_total > 0 and len(inputs[0].received) > 1): #palavras em vez de letras
        letras_corretas = 0
        letras_totais = 0
        for i in range(len_total):
            len_word =len(inputs[i].requested)
            req = inputs[i].requested
            rec = inputs[i].received
            for j in range(len_word):
                if(req[j] == rec[j]):
                    letras_corretas += 1
                letras_totais += 1
        my_dict['correct_letters_in_words'] = letras_corretas
        my_dict['acuracy_of_letters'] = letras_corretas/ letras_totais
        my_dict['total_letters'] = letras_totais
        my_dict['average_letter_per_word'] = letras_totais / len_total

    for i in inputs:
        if i.received == i.requested:
            hits = hits + [i.duration]
        total_time += i.duration
    

    n_hits = len(hits)
    n_misses = len_total - n_hits
    acuracy = 0
    dur_hit = sum(hits)
    average_time = 0
    dur_miss = 0
    time_final_str = time.ctime()
    time_final = time.time()
    time_dur = time_final - time_initial

    if(len_total != 0):
        acuracy = n_hits/len_total
        average_time = total_time / len_total
        if(n_hits == len_total):
            dur_hit = dur_hit / n_hits
        elif n_hits == 0:
            dur_miss = (total_time - dur_hit) / (len_total - n_hits)
        else:
            dur_miss = (total_time - dur_hit) / (len_total - n_hits)
            dur_hit = dur_hit/ n_hits

    my_dict['accuracy'] = acuracy
    my_dict['inputs'] = inputs
    my_dict['number_of_hits'] = n_hits
    my_dict['number_of_misses'] = n_misses
    my_dict['number_of_types'] = len_total
    my_dict['test_start'] = time_initial_str
    my_dict['test_end'] = time_final_str
    my_dict['test_duration'] = time_dur
    my_dict['type_average_duration'] = average_time
    my_dict['type_hit_average_duration'] = dur_hit
    my_dict['type_miss_average_duration'] = dur_miss

    print(Style.RESET_ALL + Back.BLACK + Fore.CYAN)
    pprint(my_dict)
    print(Back.GREEN + Fore.WHITE + "CARREGA NUMA TECLA PARA SAIR" + Style.RESET_ALL)
    exit()

# Função para escolher palavras aleatórias apartir de um ficheiro de palavras
def get_words():
    text_file = open("words.txt", "r")
    global words 
    words = text_file.read().split('\n')

def receiv_letter(qq,utm):
    global finished_event
    c = readchar.readkey()
    if(utm and finished_event.is_set()):
        return
    if qq == c:
        print(Back.BLACK + Fore.CYAN + "You typed: " + Back.GREEN + Fore.WHITE + c + Style.RESET_ALL)
    elif c==" ":
        return " "
    else:
        print(Back.BLACK + Fore.CYAN + "You typed: " + Back.RED + Fore.WHITE + c + Style.RESET_ALL + Back.BLACK + Fore.CYAN +  " instead of: " + qq + Style.RESET_ALL)
    return c

def receiv_word(word,utm):
    global finished_event
    ll = ""
    palavra = ""
    for i in range(len(word)):
        l = readchar.readkey()
        if(l == ' '):
            return l
        if(utm and finished_event.is_set()):
            return
        palavra = palavra + l
        if word[i] == l:
            ll = ll + f"{Back.GREEN}{Fore.WHITE}{l}{Style.RESET_ALL}"
        else:
            ll = ll + f"{Back.RED}{Fore.WHITE}{l}{Style.RESET_ALL}"
    
    print(Back.BLACK + Fore.CYAN, 'You typed: ' + ll, Style.RESET_ALL)
    return palavra

def gera_word():
    global words
    word = random.choice(words)
    return word

def typing_test_tries(max_value : int, gera_func, receiv_func, infinity: bool):
    global inputs
    tries = max_value
    while(tries > 0):
        initial_time = time.time()
        request = gera_func()
        print("You have" , tries , "tries")
        print(Back.BLACK + Fore.CYAN + request, " ->", Style.RESET_ALL)
        receiv = receiv_func(request,False)
        final_time = time.time()
        if(receiv == ' '):
            print(Back.RED + Fore.WHITE + "Ends with space" + Style.RESET_ALL )
            show_results("")
        if(receiv == request and infinity):
            tries += 1
        total_time = final_time - initial_time
        res = Input(requested = request, received = receiv, duration = total_time)
        inputs.append(res)
        tries -= 1
    show_results("")

def typing_test_time(max_value : int, gera_func, recebe_func, infinity : bool):
    global inputs
    global finished_event
    global max_time
    max_time = max_value
    time_max = time.time() + max_value
    # Criar a thread que indica o tempo que falta

    finished_event = threading.Event()
    finished_event.clear()
    t = threading.Thread(target = show_results_time, args = ())
    t.start()

    while not finished_event.is_set():
        request = gera_func()
        print("You have" , max_time , "seconds")
        print(Back.BLACK + Fore.CYAN + request, " ->", Style.RESET_ALL)

        initial_time = time.time()
        receiv = recebe_func(request,True)
        final_time = time.time()
        if (receiv == ' '):
            print(Back.RED + Fore.WHITE + "Ends with space" + Style.RESET_ALL)
            finished_event.set()
            exit()
        if(request == receiv and infinity):
            max_time += 1
        total_time = final_time - initial_time
        inputs.append(Input(requested = request, received = receiv, duration = total_time))
    exit()

# Funcao para selecionar a funcao de teste correta
def typing_test(utm : bool, max_value : int, uw : bool, infinity : bool):
    global time_initial_str
    global time_initial
    time_initial = time.time()
    time_initial_str = time.ctime()
    if(utm):
        if(uw):
            typing_test_time(max_value, gera_word, receiv_word, infinity)
        else:
            typing_test_time(max_value, gera_letra, receiv_letter, infinity)
    else:
        if(uw):
            typing_test_tries(max_value, gera_word, receiv_word, infinity)
        else:
            typing_test_tries(max_value, gera_letra, receiv_letter, infinity)
