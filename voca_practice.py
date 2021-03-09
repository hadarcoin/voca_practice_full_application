import random
import re
from langdetect import detect
import os
import os.path


###     CHECK EXISTING FILES AND ADDING WORDS    ###

def check_existing_files_or_create_them():
    # validation - check txt bucket exists

    file_name = 'english_bucket.txt'
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    if file_name not in file_list:
        file = open("english_bucket.txt", "w")
        file2 = open("grades_bucket.txt", "w")
        file1 = open("hebrew_bucket.txt", "w", encoding="utf-8")
    else:
        file = open("english_bucket.txt", "a")
        file2 = open("grades_bucket.txt", "a")
        file1 = open("hebrew_bucket.txt", "a", encoding="utf-8")

    return file, file2, file1


def add_words_to_buckets(english_word, hebrew_word):

    file, file2, file1 = check_existing_files_or_create_them()
    grade = 1
    #enter words to buckects
    file.write(f"{english_word},")
    file2.write(f"{grade},")
    file1.write(f"{hebrew_word},")

    file.close()
    file2.close()
    file1.close()


###     VALIDATION  - LANGUAGE CHECKER  ###

def english_checker(e_word):
    reg = re.compile(r'[a-z]')
    if reg.match(e_word):
        return 'im ok'
    else:
        return 'not english word'

def hebrew_checker(h_word):
    hebrew_check = detect(h_word)
    while hebrew_check != 'he':
        return 'not hebrew word'
    return 'im ok'


###     VALIDATION - CHECK AT LEAST 5 WORDS IN BUCKECTS  ###


def check_if_txt_buckect_is_exist():
    # validation - check txt bucket exists
    file_name = 'english_bucket.txt'
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    if file_name not in file_list:
        return "not exist"
    else:
        return "im ok"

def at_least_five_words_in_bucket():
    # validation - check if bucket empty
    e = open('english_bucket.txt', 'r')
    english_bucket = e.readlines()
    if english_bucket == []:
        return "empty bucket"
    # validation - check at least 5 words
    elif len(english_bucket[0].split(',')) <= 5:
        return "less than five words"
    else:
        return "im ok"

def validation_before_practice():
    # validation - check txt bucket exists
    english_bucket_not_exist = check_if_txt_buckect_is_exist()
    if english_bucket_not_exist == "not exist":
        return

    # validation - check at least 5 words
    at_least_five_words = at_least_five_words_in_bucket()
    if at_least_five_words == "empty bucket" or at_least_five_words == "less than five words":
        return
    else:
        return "im ok"


###     PRACTICE - PICK RANDOMLY WORDS FROM BUCKET    ###

def practice_words():

    validation_msg = validation_before_practice()
    if validation_msg == 'im ok':

        english_bucket = []
        global english_bucket1
        english_bucket1 = []
        global e
        ###   --- only read and enter to a new array called XXXX1
        e = open('english_bucket.txt', 'rt')
        english_bucket = e.readlines()
        for words in english_bucket:
            word = words.split(',')
            for i in word:
                if i == '':
                    pass
                else:
                    english_bucket1.append(i)

        grades_bucket = []
        global grades_bucket1
        grades_bucket1 = []
        global g
        g = open('grades_bucket.txt', 'rt')
        grades_bucket = g.readlines()
        for words in grades_bucket:
            word = words.split(',')
            for i in word:
                if i == '':
                    int_grades = []

                    for i in range(len(grades_bucket1)):
                        item = int(grades_bucket1[i])
                        int_grades.append(item)
                    pass
                else:
                    grades_bucket1.append(i)

        dic = {1: 5, 2: 4, 4: 2, 5: 1}
        int_grades = [dic.get(n, n) for n in int_grades]


        hebrew_bucket = []
        global hebrew_bucket1
        hebrew_bucket1 = []
        global h
        h = open('hebrew_bucket.txt', 'r', encoding="utf-8")
        hebrew_bucket = h.readlines()
        for words in hebrew_bucket:
            word = words.split(',')
            for i in word:
                if i == '':
                    pass
                else:
                    hebrew_bucket1.append(i)


        the_word = random.choices(english_bucket1, int_grades, k=1)
        #-------------------------the english word -----------------------
        the_word = the_word[0]

        global index_word
        index_word = english_bucket1.index(the_word)
        answer_array = []
        the_word_meaning = hebrew_bucket1[index_word]
        answer_array.append(the_word_meaning)

        while len(answer_array) < 5:
            hebrew_word = random.choice(hebrew_bucket1)
            if hebrew_word in answer_array:
                pass
            else:
                answer_array.append(hebrew_word)

        final_random_hebrew_words = []
        for i in range(len(answer_array)):
            h_word = random.choice(answer_array)
            final_random_hebrew_words.append(h_word)
            if h_word == hebrew_bucket1[index_word]:
                global answer_right_number
                answer_right_number = i
            h_clear_word = answer_array.index(h_word)
            del answer_array[h_clear_word]


        return the_word, final_random_hebrew_words, answer_right_number

    else:
        return 'yosi', ['a','b','c','d','e'], 2


###     UPDATE WORD'S GRADES   ###

def user_answer(num_ans):

    #num_ans --> should be the number answer the user pick in tkinter
    grade_word_change = str(grades_bucket1[index_word])
    if num_ans == str(answer_right_number):
        #pick right!
        if grade_word_change == '5':
            grade_word_change = '5'
        else:
            grade_word_change = str(int(grade_word_change) + 1)
            grades_bucket1[index_word] = grade_word_change
        update_degree()
    else:
        #pick wrong
        if grade_word_change == '1':
            grade_word_change = '1'
        else:
            grade_word_change = str(int(grade_word_change) - 1)
            grades_bucket1[index_word] = grade_word_change
        update_degree()


def update_degree():
    last_rates_arr = []
    for i in range(len(grades_bucket1)):
        if i == 0:
            num_degree = f"{grades_bucket1[i]},"
        else:
            num_degree = num_degree + f"{grades_bucket1[i]},"

    g = open('grades_bucket.txt', 'w')
    g.write(num_degree)
    g.close()


def close_files():
    e.close()
    g.close()
    h.close()





