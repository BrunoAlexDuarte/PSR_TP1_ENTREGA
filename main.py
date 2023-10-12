#!/usr/bin/env python3

import argparse

from functions import *
from colorama import Fore, Back, Style

words = []

def main():
    parser = argparse.ArgumentParser(description="Praser do typing test") 
    parser.add_argument('-utm','--use_time_mode', action='store_true',help="Put this flag if you want the test to be by time and not by tries.")
    parser.add_argument('-mv','--max_value',type=int, default = 10,help="Max number of seconds for time mode or maximum number of inputs for number of inputs mode.")
    parser.add_argument('-uw', '--use_words', action='store_true',help="Use word typing mode, instead of single character typing.")
    parser.add_argument('-inf', action='store_true',help="Infinity mode: receive 1 second or trie for each correct input")

    args = vars(parser.parse_args())
    get_words()
    global words

    print(Style.RESET_ALL + Back.BLACK + Fore.CYAN + "WELCOME TO THE TYPING TEST!")
    if(args['use_time_mode']):
        print("You will be doing the test on time mode")
        value = "seconds"
    else:
        print("You will be doing the test on tries mode")
        value = "tries"
    if(args['inf']):
        print("You will play in infinity mode")
    print("You will have", args['max_value'], value)
    print("Good luck!!")
    print("For the test to start, please press a key" + Style.RESET_ALL)
    readchar.readkey()
    typing_test(args['use_time_mode'], args['max_value'], args['use_words'], args['inf'])

    print("Ended")


if __name__ == "__main__":
    main()
