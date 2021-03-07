import tkinter as tk
import re
from tkinter import ttk
import tkinter.font as font
from voca_practice import add_words_to_buckets
from voca_practice import validation_before_practice
from voca_practice import practice_words
from voca_practice import user_answer
from high_dpi_windows import high_dpi
from voca_practice import english_checker
from voca_practice import hebrew_checker

high_dpi()

COLOR_PRIMARY = '#2e3f4f'
COLOR_SECONDARY = '#293846'
COLOR_LIGHT_BACKGROUND = 'DeepSkyBlue3'
#SlateBlue3
COLOR_LIGHT_TEXT = '#eee'
COLOR_DARK_TEXT = '#8095a8'

class MainVocaPractice(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('All_frames.TFrame', background=COLOR_LIGHT_BACKGROUND)

        style.configure(
            'LightText.TLabel', background=COLOR_PRIMARY, foreground=COLOR_LIGHT_TEXT)

        style.configure('Button_style.TButton', family='Helvetica', size=15, weight='bold')


        style.map('PomodoroButton.TButton', background=[('active', COLOR_PRIMARY), ('disabled', COLOR_LIGHT_TEXT)])

        self.title('VocaPractice')
        self.geometry('800x850')
        self.resizable(False, False)
        self.iconbitmap('IMG_4223.ico')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.frames = dict()

        container = ttk.Frame(self, width=700, height=750)
        container.pack(fill='both', expand=True, padx=20, pady=20)

        for FrameClass in (Menu, Practice, AddWords):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky='NESW', ipadx=20, ipady=20)

        self.show_frame(Menu)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        if frame == self.frames[Practice]:
            self.frames[Practice].suffle_words()
        if frame == self.frames[AddWords]:
            self.frames[AddWords].delete_existing()
        #if frame == self.frames[Menu]:
        #    #validation_before_practice()
        #    message = validation_before_practice()
        #    if message == 'im ok':
        #        pass
        #    else:
        #        self.frames[Menu].switch_page_button_to_practice['state'] = "disabled"
        #        self.frames[Menu].message_label_variable.set('Please add at least 5 words before practice!')


class Menu(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)


        style = ttk.Style()
        self['style'] = 'All_frames.TFrame'
        titlefont = font.Font(family='Helvetica', size=20, weight='bold')
        explainfont = font.Font(family='Helvetica', size=12, weight='bold')
        style.configure('TButton', background='seashell3', foreground='black', width=20, borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', 'SlateBlue4'), ('disabled', 'red')], foreground=[('active', 'white')])

        self.message_label_variable = tk.StringVar()


        # --  widgets  --
        main_title_label = ttk.Label(self, text='Voca Practice', font=titlefont, background='DeepSkyBlue3', anchor='center',width=35)
        explain_label = ttk.Label(self, text='Voca Practice is an application for practice your vocabulary.\nThe application '
                                             'exam your knowledge in a smart way.\nGiving grades for '
                                             'each one of the words.\nIn that way, the application promise '
                                             'you will practice the words\nyou less familiar with.\n\nEnjoy '
                                             ': )', font=explainfont, foreground='SlateBlue4', background='DeepSkyBlue3', padding=(2,40,2,215))
        message_label = ttk.Label(self, textvariable=self.message_label_variable, font=explainfont, foreground='red', background='DeepSkyBlue3')
        switch_page_button_to_add_words = ttk.Button(self, text='Add words', style='TButton',width=45,
                                        command=lambda: controller.show_frame(AddWords))
        switch_page_button_to_practice = ttk.Button(self, text='Practice',width=45,
                                        command=lambda: controller.show_frame(Practice))

        # --  layouts  --
        main_title_label.grid(column=0, row=0, columnspan=3, sticky='ew')
        explain_label.grid(column=0, row=3, columnspan=3, sticky='ew')
        message_label.grid(column=0, row=4, columnspan=2, sticky='ew')
        switch_page_button_to_add_words.grid(column=0, row=5, columnspan=2, sticky='ew')
        switch_page_button_to_practice.grid(column=0, row=6, columnspan=2, sticky='ew')

        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)


        message = validation_before_practice()
        if message == 'im ok':
            pass
        else:
            switch_page_button_to_practice['state'] = "disabled"
            self.message_label_variable.set('Please add at least 5 words before practice!')

   #def refresh_validation_message(self):
   #    message = validation_before_practice()
   #    if message == 'im ok':
   #        pass
   #    else:
   #        self.switch_page_button_to_practice['state'] = "disabled"
   #        self.message_label_variable.set('Please add at least 5 words before practice!')




class Practice(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        style = ttk.Style()
        self['style'] = 'All_frames.TFrame'
        wordfont = font.Font(family='Helvetica', size=20, weight='bold')
        style.configure('Wild.TRadiobutton', background='orange', foreground='black', width=20, borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('Wild.TRadiobutton', background=[('active', 'dark orange')], foreground=[('active', 'white')])
        style.configure("BW.TLabel", foreground="black", background="DeepSkyBlue3")

        the_word, answer_arr, answer_right_number = practice_words()


        self.the_word = tk.StringVar(value=the_word)
        self.storage_user_choose = tk.StringVar()
        self.result = tk.StringVar()
        self.word1 = tk.StringVar(value=answer_arr[0])
        self.word2 = tk.StringVar(value=answer_arr[1])
        self.word3 = tk.StringVar(value=answer_arr[2])
        self.word4 = tk.StringVar(value=answer_arr[3])
        self.word5 = tk.StringVar(value=answer_arr[4])
        self.answer_right_number = tk.StringVar(value=answer_right_number)
        self.answer_arr = tk.StringVar(value=answer_arr)

        # --  widgets  --

        the_shown_word = ttk.Label(self, textvariable=self.the_word, anchor='center', font=wordfont, background='DeepSkyBlue3', padding=(0,5,30,10))

        first_word = ttk.Radiobutton(self, textvariable=self.word1,  variable=self.storage_user_choose, value=0, style='Wild.TRadiobutton')
        second_word = ttk.Radiobutton(self, textvariable=self.word2, variable=self.storage_user_choose, value=1, style='Wild.TRadiobutton')
        third_word = ttk.Radiobutton(self, textvariable=self.word3,  variable=self.storage_user_choose, value=2, style='Wild.TRadiobutton')
        fourth_word = ttk.Radiobutton(self, textvariable=self.word4, variable=self.storage_user_choose, value=3, style='Wild.TRadiobutton')
        fifth_word = ttk.Radiobutton(self, textvariable=self.word5,  variable=self.storage_user_choose, value=4, style='Wild.TRadiobutton')

        result_label = ttk.Label(self, textvariable=self.result, background='DeepSkyBlue3', style="BW.TLabel",width=43)

        check_button = ttk.Button(self, text='Check', command=self.check_if_correct)

        again_button = ttk.Button(self, text='Next word', command=self.suffle_words)

        switch_page_button = ttk.Button(self, text=' Back to Main',
                                        command=lambda: controller.show_frame(Menu))

        # --  layouts  --

        the_shown_word.grid(column=1, row=1, columnspan=2, sticky='EW')

        first_word.grid(column=1, row=2, sticky='W')
        second_word.grid(column=1, row=3, sticky='W')
        third_word.grid(column=1, row=4, sticky='W')
        fourth_word.grid(column=1, row=5, sticky='W')
        fifth_word.grid(column=1, row=6, sticky='W')

        result_label.grid(column=0, row=7, columnspan=2, sticky='ew')
        check_button.grid(column=0, row=8, columnspan=2, sticky='ew')
        again_button.grid(column=0, row=9, columnspan=2, sticky='ew')

        switch_page_button.grid(column=0, row=10, columnspan=2, sticky='ew')


        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)


    def check_if_correct(self, *args):

        word_num = self.storage_user_choose.get()
        answer_right_number = int(self.answer_right_number.get())
        answer_arr = self.answer_arr.get()

        answer_arr = re.sub(r'[(,)]','', answer_arr).replace(" ",',')
        answer_arr = answer_arr.replace("\\", "")
        answer_arr = answer_arr.replace("'",'')
        answer_arr = answer_arr.split(',')

        #just update the backend code for update the grades of the words
        user_answer(word_num)
        if int(word_num) == answer_right_number:
            self.result.set(f'Right answer !!')
        else:
            self.result.set(f'Wrong! the right answer is: {answer_arr[answer_right_number]}')


    def suffle_words(self):
        self.storage_user_choose.set('')
        new_the_word, new_answer_arr, new_answer_right_number = practice_words()
        self.the_word.set(new_the_word)
        self.word1.set(new_answer_arr[0])
        self.word2.set(new_answer_arr[1])
        self.word3.set(new_answer_arr[2])
        self.word4.set(new_answer_arr[3])
        self.word5.set(new_answer_arr[4])
        self.answer_right_number.set(new_answer_right_number)
        self.answer_arr.set(new_answer_arr)
        self.result.set('')



class AddWords(ttk.Frame):
    def __init__(self, container, controller, **kwargs):
        super().__init__(container, **kwargs)

        style = ttk.Style()
        self['style'] = 'All_frames.TFrame'
        style.configure("BW.TLabel", foreground="black", background="DeepSkyBlue3")
        style.configure("BW.TLabel_if_error", foreground="red", background="DeepSkyBlue3")
        style.configure("EntryStyle.TEntry", background='orange')
        style.map("EntryStyle.TEntry", foreground=[('disabled', 'yellow'), ('active', 'blue')], background=[(
            'disabled', 'magenta'), ('active', 'green')], highlightcolor=[('focus', 'green'), ('!focus', 'red')])


        self.english_user_input = tk.StringVar()
        self.hebrew_user_input = tk.StringVar()
        self.print_message = tk.StringVar()


        # --  widgets  --

        english_label = ttk.Label(self, text='English word:', style="BW.TLabel")
        enter_english = ttk.Entry(self, textvariable=self.english_user_input, style="EntryStyle.TEntry")
        hebrew_label = ttk.Label(self, text='Hebrew word:', style="BW.TLabel")
        enter_hebrew = ttk.Entry(self, textvariable=self.hebrew_user_input, style="EntryStyle.TEntry")

        print_label = ttk.Label(self, textvariable=self.print_message, style="BW.TLabel", foreground='white')

        insert_button = ttk.Button(self, text='Submit', command=self.insert, width=45,)

        switch_page_button = ttk.Button(self, text=' Back to Main',width=45,
                                        command=lambda: controller.show_frame(Menu))

        # --  layouts  --
        english_label.grid(column=0, row=1, sticky='w')
        enter_english.grid(column=1, row=1, sticky='ew')
        hebrew_label.grid(column=0, row=2, sticky='w')
        enter_hebrew.grid(column=1, row=2, sticky='ew')

        print_label.grid(column=0, row=3, columnspan=2, sticky='ew')

        insert_button.grid(column=0, row=4, columnspan=2, sticky='ew')

        switch_page_button.grid(column=0, row=5, columnspan=2, sticky='ew')


        for child in self.winfo_children():
            child.grid_configure(padx=15, pady=15)

    def checker_words_language(self, e_word, h_word):
        result_english = english_checker(e_word)
        result_hebrew = hebrew_checker(h_word)
        return result_english, result_hebrew


    def insert(self, *args, **kwargs):
        e_word = self.english_user_input.get()
        h_word = self.hebrew_user_input.get()

        result_e, result_h = self.checker_words_language(e_word, h_word)
        if result_e == 'im ok' and result_h == 'im ok':
            add_words_to_buckets(e_word, h_word)
            self.print_message.set(f'{e_word} : {h_word} are added!')
            self.english_user_input.set("")
            self.hebrew_user_input.set("")
        else:
            #self.change_color_label()
            #want to change color to red
            if result_e == 'im ok' and result_h != 'im ok':
                self.print_message.set('Please correct your Hebrew word!')
            elif result_e != 'im ok' and result_h == 'im ok':
                self.print_message.set('Please correct your English word!')


    def delete_existing(self, *args):
        self.print_message.set("")





root = MainVocaPractice()

font.nametofont('TkDefaultFont').configure(size=15)

root.mainloop()