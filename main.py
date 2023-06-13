import random
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import pyttsx3

import base


class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title('Work out of english words 3000')
        self.root.geometry('860x670+300+100')

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        # наполняем комбобокс с подгруппами
        self.options = base.get_subgroups()

        frame_left = ctk.CTkFrame(self.root)
        frame_left.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 25))

        tabview = ctk.CTkTabview(frame_left)
        tabview.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 15))
        tab_write = tabview.add('Step 1. Write the correct translation')
        tab_choice = tabview.add('Step 2. Choose the correct translation')

        frame_filter_set = ctk.CTkFrame(frame_left)
        frame_filter_set.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 0))
        var1 = ctk.StringVar()
        self.combo_group = ctk.CTkComboBox(frame_filter_set, variable=var1, width=270,
                                           values=tuple(self.options.keys()), command=self.combo_subgroup_selected)
        self.combo_group.grid(row=0, column=0, columnspan=3, sticky='w', padx=5, pady=10)
        self.combo_group.set('существительные')
        var2 = ctk.StringVar()
        var3 = ctk.StringVar()
        self.combo_subgroup = ctk.CTkComboBox(frame_filter_set, width=200, variable=var2, command=self.combo_set_selected)
        self.combo_subgroup.grid(row=0, column=3, sticky='w', padx=5, pady=10)
        self.combo_subgroup.set('армия')
        self.combo_set = ctk.CTkComboBox(frame_filter_set, width=60, variable=var3, values=['1'])
        self.combo_set.grid(row=0, column=4, padx=5, pady=10)
        self.combo_set.set('1')
        check_var = BooleanVar()
        check_var.set(True)
        self.status_unknow = ctk.CTkCheckBox(frame_filter_set, variable=check_var, text='не знаю')
        self.status_unknow.grid(row=1, column=0, pady=10, padx=(10, 0))
        self.status_repeat = ctk.CTkCheckBox(frame_filter_set, text='повтор')
        self.status_repeat.grid(row=1, column=1, pady=10)
        self.status_know = ctk.CTkCheckBox(frame_filter_set, text='знаю')
        self.status_know.grid(row=1, column=2, pady=10)
        ctk.CTkButton(frame_filter_set, text='show my collection',
                      command=self.get_treeview_dictionary).grid(row=1, column=3, columnspan=2, sticky='e', padx=5,
                                                                 pady=10)
        self.set_words = ctk.CTkLabel(frame_filter_set, text='', font=('Areal', 20, 'bold'))
        self.set_words.grid(row=2, column=0, columnspan=5, pady=(10, 10))

        self.root.bind("<Shift_R>", self.start_workout_write)
        self.root.bind("<Return>", self.get_result_workout_write)

        frame_workout_write = ctk.CTkFrame(tab_write)
        frame_workout_write.pack(pady=10)
        ctk.CTkLabel(frame_workout_write, text='Write the correct translation:', font=('Areal', 20)).pack(padx=5,
                                                                                                          pady=(5, 5))
        ctk.CTkLabel(frame_workout_write, text="Work with hotkeys: 'Shift_R'- new word, 'Enter'- check'",
                     font=('Areal', 12)).pack(padx=30, pady=20)

        frame_board_for_writing = ctk.CTkFrame(frame_workout_write)
        frame_board_for_writing.pack(padx=(20, 20), fill='both', expand=True)
        self.show_rusword_label = ctk.CTkLabel(frame_board_for_writing, width=250, text='',
                                               font=('Areal', 22, 'bold'), text_color='green', justify=tk.CENTER)
        self.show_rusword_label.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 10))
        self.correct_engword_for_check = ctk.CTkEntry(frame_board_for_writing, width=250, justify=tk.CENTER)
        self.var = StringVar()
        self.try_engword_entry = ctk.CTkEntry(frame_board_for_writing, width=250, textvariable=self.var,
                                              justify=tk.CENTER)
        self.try_engword_entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(10, 20))
        self.show_result_write_label = ctk.CTkLabel(frame_workout_write, text='')
        self.show_result_write_label.pack(padx=(20, 20), pady=(20, 20))

        frame_workout_choice = ctk.CTkFrame(tab_choice)
        frame_workout_choice.pack(pady=10)
        ctk.CTkLabel(frame_workout_choice, text='Choose the workout settings:', font=('Areal', 20)).pack(pady=(10, 0))

        frame_option_workout_choice = ctk.CTkFrame(frame_workout_choice)
        frame_option_workout_choice.pack(padx=(20, 20), pady=(5, 5))
        self.var_voice_write = IntVar()
        self.var_voice_write.set(1)
        written = ctk.CTkRadioButton(frame_option_workout_choice, text='in written', variable=self.var_voice_write,
                                     value=1)
        written.grid(row=0, column=0, padx=(10, 10), pady=(5, 5))
        orally = ctk.CTkRadioButton(frame_option_workout_choice, text='orally', variable=self.var_voice_write, value=2)
        orally.grid(row=1, column=0, padx=(10, 10), pady=(5, 5))
        self.word_for_sound = ctk.CTkLabel(frame_option_workout_choice, text='1')
        self.var_translation_direction = IntVar()
        self.var_translation_direction.set(1)
        ru_eng = ctk.CTkRadioButton(frame_option_workout_choice, text='ru-eng', variable=self.var_translation_direction,
                                    value=1)
        ru_eng.grid(row=0, column=1, padx=(10, 10), pady=(5, 5))
        eng_ru = ctk.CTkRadioButton(frame_option_workout_choice, text='eng-ru', variable=self.var_translation_direction,
                                    value=2)
        eng_ru.grid(row=1, column=1, padx=(10, 10), pady=(5, 5))

        self.correct_translate_word_label = ctk.CTkLabel(frame_workout_choice, text='')
        self.try_choice_user_label = ctk.CTkLabel(frame_workout_choice, text='')

        frame_bottom_btn = ctk.CTkFrame(frame_workout_choice)
        frame_bottom_btn.pack(side=BOTTOM, padx=(10, 10), pady=(5, 5))
        ctk.CTkButton(frame_bottom_btn, text='Listen', font=('Areal', 18),
                      command=self.get_sound).grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
        ctk.CTkButton(frame_bottom_btn, text='New word', font=('Areal', 18),
                      command=self.start_workout_choice).grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

        self.show_result_choice_label = ctk.CTkLabel(frame_workout_choice, text='')
        self.show_result_choice_label.pack(side=BOTTOM, padx=(20, 20))

        frame_box_for_choice = ctk.CTkFrame(frame_workout_choice)
        frame_box_for_choice.pack()
        self.random_word_for_workout_label = ctk.CTkLabel(frame_box_for_choice, text='',
                                                          font=('Areal', 22, 'bold'), text_color='green')
        self.random_word_for_workout_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
        self.word1 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                                   command=lambda: self.get_result_workout_choice(self.word1))
        self.word1.grid(row=1, column=0, padx=10, pady=10)
        self.word2 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                                   command=lambda: self.get_result_workout_choice(self.word2))
        self.word2.grid(row=2, column=0, padx=10, pady=10)
        self.word3 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                                   command=lambda: self.get_result_workout_choice(self.word3))
        self.word3.grid(row=1, column=1, padx=10, pady=10)
        self.word4 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                                   command=lambda: self.get_result_workout_choice(self.word4))
        self.word4.grid(row=2, column=1, padx=10, pady=10)

        frame_right = ctk.CTkFrame(self.root)
        frame_right.grid(row=0, column=3, pady=15, padx=(0, 15), sticky='n')
        frame_statistics = ctk.CTkFrame(frame_right)
        frame_statistics.grid(row=0, column=0, pady=15, padx=15, sticky='n')
        ctk.CTkLabel(frame_statistics, text='Statistics:',
                     font=('Areal', 18, 'bold')).grid(row=0, column=0, padx=(10, 10), pady=(10, 0))
        start_text_statistic = '''
                know - 0 (0%), 
                repeat - 0 (0%), 
                don't know - 0 (0%)'''
        self.statistic_status = ctk.CTkLabel(frame_statistics, text=start_text_statistic, font=('Areal', 13),
                                             justify=tk.LEFT)
        self.statistic_status.grid(row=1, column=0, pady=(0, 10), padx=(0, 10))
        ctk.CTkButton(frame_statistics, text='Update statistics',
                      command=self.get_statistics).grid(row=2, column=0, padx=15, pady=15)

        frame_update_status = ctk.CTkFrame(frame_right)
        frame_update_status.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky='nesw')
        ctk.CTkLabel(frame_update_status, text='Update status:', font=('Areal', 18, 'bold')).pack(padx=(10, 10),
                                                                                                  pady=(20, 10))
        self.var_status = StringVar()
        self.var_status.set('не знаю')
        status_unknow_radio = ctk.CTkRadioButton(frame_update_status, text='не знаю', variable=self.var_status,
                                                 value='не знаю')
        status_unknow_radio.pack(padx=(10, 10), pady=(5, 5))
        status_repeat_radio = ctk.CTkRadioButton(frame_update_status, text='повтор', variable=self.var_status,
                                                 value='повтор')
        status_repeat_radio.pack(padx=(10, 10), pady=(5, 5))
        status_know_radio = ctk.CTkRadioButton(frame_update_status, text='знаю', variable=self.var_status, value='знаю')
        status_know_radio.pack(padx=(10, 10), pady=(5, 5))
        ctk.CTkButton(frame_update_status, text='Change status of set',
                      command=self.update_status).pack(padx=(10, 10), pady=(15, 5))
        ctk.CTkButton(frame_update_status, text='Full "не знаю"-status',
                      command=self.update_status_all).pack(padx=(10, 10), pady=(5, 15))

        frame_appearance_mode = ctk.CTkFrame(frame_right)
        frame_appearance_mode.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky='nesw')

        appearance_mode_label = ctk.CTkLabel(frame_appearance_mode, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = ctk.CTkOptionMenu(frame_appearance_mode, values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.set('Dark')
        appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))

    def run(self):
        self.get_statistics()
        self.root.mainloop()

    # ------------------------------------FILTER OF WORD'S SET----------------------------------------------------------

    # создание всплывающего окна с выборкой слов
    def open_toplevel_window(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Dictionary")
        dialog.geometry('350x300+700+400')
        dialog.grab_set()

        def work_out():
            dialog.destroy()
            self.word1.configure(text='')
            self.word2.configure(text='')
            self.word3.configure(text='')
            self.word4.configure(text='')

        ctk.CTkButton(dialog, text='Work out', command=work_out).pack(side=BOTTOM, pady=20)
        return dialog

    # вывод таблицы с выборкой слов во всплывающее окно
    def get_treeview_dictionary(self):
        dictionary = self.get_dictionary()
        tab_dictionary = []
        for i in dictionary:
            tab_dictionary.append((i, dictionary[i]))
        columns = ("rusword", "engword")

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, background="#D3D3D3", font=('Calibri', 13))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        dial = self.open_toplevel_window()
        tree = ttk.Treeview(master=dial, height=15, columns=columns, show="headings", style="mystyle.Treeview")
        tree.pack()

        tree.heading("rusword", text="RUSWORD")
        tree.heading("engword", text="ENGWORD")

        for i in tab_dictionary:
            tree.insert("", END, values=i)

    def combo_subgroup_selected(self, value):
        values = self.options[value]
        self.combo_subgroup.configure(values=values)
        self.combo_subgroup.set('')

    def combo_set_selected(self, value):
        values = base.get_sets(self.combo_group.get(), value)
        self.combo_set.configure(values=values)
        self.combo_set.set('')

    # ----------------------------WORKOUT - TO WRITE TRANSLATE--------------------------------------------------
    def start_workout_write(self, event):
        self.clean_fields()
        dictionary = self.get_dictionary()
        if dictionary != {}:
            rus = random.choice(list(dictionary))
            self.show_rusword_label.configure(text=rus)
            engword = dictionary.get(rus)
            self.correct_engword_for_check.configure(placeholder_text=engword)
        else:
            messagebox.showerror(title='Empty set', message='Empty set! Choice other set!')

    def get_correct_word_workout_write(self):
        word = self.correct_engword_for_check.cget('placeholder_text')
        if word.startswith('('):
            correct_word = word[word.find(')') + 1:].strip()
        elif '(' in word:
            correct_word = word[:word.find('(')].strip()
        else:
            correct_word = word
        return correct_word

    def get_result_workout_write(self, event):
        correct_word = self.get_correct_word_workout_write()
        try_word = self.var.get()
        if correct_word == try_word:
            msg = f"OK, good job!      {self.show_rusword_label.cget('text')} - {correct_word.upper()}"
            self.show_result_write_label.configure(text=msg, text_color='green')
        else:
            msg = f"Fail, correct:      {self.show_rusword_label.cget('text')} - {correct_word.upper()}"
            self.show_result_write_label.configure(text=msg, text_color='red')

    # ----------------------------WORKOUT - TO CHOICE TRANSLATE----------------------------------------------
    def clean_fields(self):
        # clean choice workout
        self.try_choice_user_label.configure(text='')
        self.correct_translate_word_label.configure(text='')
        self.show_result_choice_label.configure(text='')
        self.word_for_sound.configure(text='')
        # clean write workout
        self.show_rusword_label.configure(text='')
        self.show_result_write_label.configure(text='')
        self.try_engword_entry.delete(0, last_index=300)

    # получаем выборку из словаря РАЗДЕЛИТЬ
    def get_dictionary(self):
        self.set_words.configure(
            text=f' {self.combo_group.get()} - {self.combo_subgroup.get()} (set {self.combo_set.get()})')
        group_set = self.combo_group.get()
        subgroup_set = self.combo_subgroup.get()
        set_n = int(self.combo_set.get())
        a, b, c = '', '', ''
        if self.status_know.get() == True:
            a = 'знаю'
        if self.status_unknow.get() == True:
            b = 'не знаю'
        if self.status_repeat.get() == True:
            c = 'повтор'

        with sqlite3.connect('app.db') as db:
            cursor = db.cursor()
            query = """
                    SELECT rusword, engword
                    FROM dictionary
                    WHERE set_n = ? AND subgroup = ? AND group_part = ? 
                    AND (status = ? OR status = ? OR status = ?);
                    """
            cursor.execute(query, (set_n, subgroup_set, group_set, a, b, c))
            dictionary_set = {}
            for res in cursor:
                dictionary_set[res[1]] = res[0]
        return dictionary_set

    # озвучивание слов РАЗДЕЛИТЬ
    def get_sound(self):
        word = self.word_for_sound.cget('text')
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 120)
        engine.setProperty('volume', 0.9)
        engine.say(word)
        engine.runAndWait()

    def get_dictionary_by_translation_direction(self):
        '''упростить код'''
        dictionary = self.get_dictionary()
        if self.var_translation_direction.get() == 2:  # eng-ru
            dictionary = {value: key for key, value in dictionary.items()}
        return dictionary

    def get_written_or_voice_method(self, random_word_for_workout):
        if self.var_voice_write.get() == 1:  # in write
            self.random_word_for_workout_label.configure(text=random_word_for_workout)
        if self.var_voice_write.get() == 2:  # orally
            self.random_word_for_workout_label.configure(text="")
            self.get_sound()

    def start_workout_choice(self):
        self.clean_fields()
        dictionary = self.get_dictionary_by_translation_direction()

        if dictionary == {}:
            messagebox.showerror(title='Empty set', message='Empty set! Choice other set!')
        else:
            random_word_for_workout = random.choice(list(dictionary))
            correct_translate_word = dictionary.get(random_word_for_workout)
            self.correct_translate_word_label.configure(text=correct_translate_word)

            if self.var_translation_direction.get() == 1:  # ru-eng
                self.word_for_sound.configure(text=correct_translate_word)
            else:
                self.word_for_sound.configure(text=random_word_for_workout)

            self.show_translation_options_on_buttons(dictionary, correct_translate_word, random_word_for_workout)
            self.get_written_or_voice_method(random_word_for_workout)

    def show_translation_options_on_buttons(self, dictionary, correct_word, random_word_for_workout):
        # correct word on button
        btns = [self.word1, self.word2, self.word3, self.word4]
        btn = random.choice(btns)
        btn.configure(text=correct_word)
        btns.remove(btn)
        dictionary.pop(random_word_for_workout)
        # other options on buttons
        while not btns == []:
            btn = random.choice(btns)
            other_option = random.choice(list(dictionary))
            other_translate = dictionary.get(other_option)
            btn.configure(text=other_translate)
            dictionary.pop(other_option)
            btns.remove(btn)

    def get_result_workout_choice(self, btn):
        self.try_choice_user_label.configure(text=btn.cget('text'))
        self.show_result_workout_choice()

    def show_result_workout_choice(self):
        eng = self.correct_translate_word_label.cget('text')
        word = self.try_choice_user_label.cget('text')
        if word == eng:
            msg = f"OK, good job! It's      {eng.upper()}"
            self.show_result_choice_label.configure(text=msg, text_color='green')
        else:
            msg = f"Fail, correct:     {self.random_word_for_workout_label.cget('text')} - {eng.upper()}"
            self.show_result_choice_label.configure(text=msg, text_color='red')

    # ----------------------------------STATISTIC----------------------------------------------------------

    # получаем статистику по статусам слов РАЗДЕЛИТЬ
    def get_statistics(self):
        with sqlite3.connect('app.db') as db:
            cursor = db.cursor()
            query = """
                    SELECT status, count(engword)  
                    FROM dictionary
                    GROUP BY status;
                    """
            cursor.execute(query)
            count_words_in_set = {}
            for res in cursor:
                count_words_in_set[res[0]] = str(res[1])
                a = int(count_words_in_set.get('не знаю')) if count_words_in_set.get('не знаю') else 0
                b = int(count_words_in_set.get('повтор')) if count_words_in_set.get('повтор') else 0
                c = int(count_words_in_set.get('знаю')) if count_words_in_set.get('знаю') else 0
                if a + b + c != 0:
                    a_per = round(a / (a + b + c) * 100)
                    b_per = round(b / (a + b + c) * 100)
                    c_per = round(c / (a + b + c) * 100)
        new_statistics = f'''
        know - {c} ({c_per}%), 
        repeat - {b} ({b_per}%), 
        don't know - {a} ({a_per}%)'''
        self.statistic_status.configure(text=new_statistics)

    # ----------------------------------UPDATE STATUS----------------------------------------------------------

    # обнуление всех статусов
    def update_status_all(self):
        msg = '''Вы собираетесь все статусы в словаре изменить на "НЕ ЗНАЮ". 
        Это необратимый процесс. Продолжить?'''
        ans_question1 = messagebox.askquestion(title='Full update status', message=msg)
        if ans_question1 == 'yes':
            with sqlite3.connect('app.db') as db:
                cursor = db.cursor()
                query = """
                            UPDATE dictionary
                            SET status = 'не знаю'
                            """
                cursor.execute(query)
                messagebox.showinfo(title='Full update status', message='Status on "не знаю" updated successfully!')

    # редактирование статуса слов в сете
    def update_status(self):
        group_set = self.combo_group.get()
        subgroup_set = self.combo_subgroup.get()
        set_n = int(self.combo_set.get())
        new_status = self.var_status.get()
        with sqlite3.connect('app.db') as db:
            cursor = db.cursor()
            query = """
                        UPDATE dictionary
                        SET status = ?
                        WHERE set_n = ? AND subgroup = ? AND group_part = ? 
                        """
            cursor.execute(query, (new_status, set_n, subgroup_set, group_set))
            messagebox.showinfo(title='Status update', message='Status updated successfully!')

    # ----------------------------------APPEARANCE MODE----------------------------------------------------------

    def change_appearance_mode_event(self, event):
        ctk.set_appearance_mode(event)


if __name__ == '__main__':
    MainWindow().run()
