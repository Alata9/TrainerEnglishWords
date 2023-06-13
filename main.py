import random
import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import pyttsx3




root = ctk.CTk()
root.title('Work out of english words 3000')
root.geometry('860x670+300+100')

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")




#------------------------------------FILTER OF WORD'S SET----------------------------------------------------------

# создание всплывающего окна с выборкой слов
def open_toplevel_window():
    dialog = ctk.CTkToplevel(root)
    dialog.title("Dictionary")
    dialog.geometry('350x300+700+400')
    dialog.grab_set()
    def work_out():
        dialog.destroy()
        word1.configure(text='')
        word2.configure(text='')
        word3.configure(text='')
        word4.configure(text='')
    ctk.CTkButton(dialog, text='Work out', command=work_out).pack(side=BOTTOM, pady=20)
    return dialog

# вывод таблицы с выборкой слов во всплывающее окно
def get_treeview_dictionary():
    dictionary = get_dictionary()
    tab_dictionary = []
    for i in dictionary:
        tab_dictionary.append((i, dictionary[i]))
    columns = ("rusword", "engword")

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, background="#D3D3D3", font=('Calibri', 13))
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 20, 'bold'))
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

    dial = open_toplevel_window()
    tree = ttk.Treeview(master=dial, height=15, columns=columns, show="headings", style="mystyle.Treeview")
    tree.pack()

    tree.heading("rusword", text="RUSWORD")
    tree.heading("engword", text="ENGWORD")

    for i in tab_dictionary:
        tree.insert("", END, values=i)


# получили полный список групп-подгрупп для комбобоксов
def get_subgroups():
    with sqlite3.connect('app.db') as db:
        cursor = db.cursor()
        query = """
                SELECT group_id, subgroup 
                FROM subgroups
                """
        cursor.execute(query)
    subgroups = {}
    for res in cursor:
        if res[0] in subgroups:
            subgroups[res[0]] += (res[1],)
        else:
            subgroups[res[0]] = (res[1],)
    return subgroups


# наполняем комбобокс с подгруппами
options = get_subgroups()
def combo_subgroup_selected(value):
    values = options[value]
    combo_subgroup.configure(values=values)
    combo_subgroup.set('')

frame_left = ctk.CTkFrame(root)
frame_left.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 25))

tabview = ctk.CTkTabview(frame_left)
tabview.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 15))
tab_write = tabview.add('Step 1. Write the correct translation')
tab_choice = tabview.add('Step 2. Choose the correct translation')

frame_filter_set = ctk.CTkFrame(frame_left)
frame_filter_set.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=15, pady=(15, 0))
var1 = ctk.StringVar()
combo_group = ctk.CTkComboBox(frame_filter_set, variable=var1, width=270,
                              values=tuple(options.keys()), command=combo_subgroup_selected)
combo_group.grid(row=0, column=0, columnspan=3, sticky='w', padx=5, pady=10)
combo_group.set('существительные')
var2 = ctk.StringVar()
combo_subgroup = ctk.CTkComboBox(frame_filter_set, width=200, variable=var2)
combo_subgroup.grid(row=0, column=3, sticky='w', padx=5, pady=10)
combo_subgroup.set('армия')
combo_set = ctk.CTkComboBox(frame_filter_set, width=60, values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])
combo_set.grid(row=0, column=4, padx=5, pady=10)
combo_set.set('1')
check_var = BooleanVar()
check_var.set(True)
status_unknow = ctk.CTkCheckBox(frame_filter_set, variable=check_var, text='не знаю')
status_unknow.grid(row=1, column=0, pady=10, padx=(10, 0))
status_repeat = ctk.CTkCheckBox(frame_filter_set, text='повтор')
status_repeat.grid(row=1, column=1, pady=10)
status_know = ctk.CTkCheckBox(frame_filter_set, text='знаю')
status_know.grid(row=1, column=2, pady=10)
ctk.CTkButton(frame_filter_set, text='show my collection',
              command=get_treeview_dictionary).grid(row=1, column=3, columnspan=2, sticky='e', padx=5, pady=10)
set_words = ctk.CTkLabel(frame_filter_set, text='', font=('Areal', 20, 'bold'))
set_words.grid(row=2, column=0, columnspan=5, pady=(10, 10))



# ----------------------------WORKOUT - TO WRITE TRANSLATE--------------------------------------------------
def start_workout_write(event):
    clean_fields()
    dictionary = get_dictionary()
    if dictionary != {}:
        rus = random.choice(list(dictionary))
        show_rusword_label.configure(text=rus)
        engword = dictionary.get(rus)
        correct_engword_for_check.configure(placeholder_text=engword)
    else:
        messagebox.showerror(title='Empty set', message='Empty set! Choice other set!')

root.bind("<Shift_R>", start_workout_write)


def get_correct_word_workout_write():
    word = correct_engword_for_check.cget('placeholder_text')
    if word.startswith('('):
        correct_word = word[word.find(')') + 1:].strip()
    elif '(' in word:
        correct_word = word[:word.find('(')].strip()
    else:
        correct_word = word
    return correct_word


def get_result_workout_write(event):
    correct_word = get_correct_word_workout_write()
    try_word = var.get()
    if correct_word == try_word:
        msg = f"OK, good job!      {show_rusword_label.cget('text')} - {correct_word.upper()}"
        show_result_write_label.configure(text=msg, text_color='green')
    else:
        msg = f"Fail, correct:      {show_rusword_label.cget('text')} - {correct_word.upper()}"
        show_result_write_label.configure(text=msg, text_color='red')

root.bind("<Return>", get_result_workout_write)


frame_workout_write = ctk.CTkFrame(tab_write)
frame_workout_write.pack(pady=10)
ctk.CTkLabel(frame_workout_write, text='Write the correct translation:', font=('Areal', 20)).pack(padx=5, pady=(5, 5))
ctk.CTkLabel(frame_workout_write, text="Work with hotkeys: 'Shift_R'- new word, 'Enter'- check'",
             font=('Areal', 12)).pack(padx=30, pady=20)

frame_board_for_writing = ctk.CTkFrame(frame_workout_write)
frame_board_for_writing.pack(padx=(20, 20), fill='both', expand=True)
show_rusword_label = ctk.CTkLabel(frame_board_for_writing, width=250, text='',
                                  font=('Areal', 22, 'bold'), text_color='green', justify=tk.CENTER)
show_rusword_label.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 10))
correct_engword_for_check = ctk.CTkEntry(frame_board_for_writing, width=250, justify=tk.CENTER)
var = StringVar()
try_engword_entry = ctk.CTkEntry(frame_board_for_writing, width=250, textvariable=var, justify=tk.CENTER)
try_engword_entry.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(10, 20))
show_result_write_label = ctk.CTkLabel(frame_workout_write, text='')
show_result_write_label.pack(padx=(20, 20), pady=(20, 20))


# ----------------------------WORKOUT - TO CHOICE TRANSLATE----------------------------------------------
def clean_fields():
    # clean choice workout
    try_choice_user_label.configure(text='')
    correct_translate_word_label.configure(text='')
    show_result_choice_label.configure(text='')
    word_for_sound.configure(text='')
    # clean write workout
    show_rusword_label.configure(text='')
    show_result_write_label.configure(text='')
    try_engword_entry.delete(0, last_index=300)


# получаем выборку из словаря
def get_dictionary():
    set_words.configure(text=f' {combo_group.get()} - {combo_subgroup.get()} (set {combo_set.get()})')
    group_set = combo_group.get()
    subgroup_set = combo_subgroup.get()
    set_n = int(combo_set.get())
    a, b, c = '', '', ''
    if status_know.get() == True:
        a = 'знаю'
    if status_unknow.get() == True:
        b = 'не знаю'
    if status_repeat.get() == True:
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

# озвучивание слов
def get_sound():
    word = word_for_sound.cget('text')
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 0.9)
    engine.say(word)
    engine.runAndWait()


def get_dictionary_by_translation_direction():
    '''упростить код'''

    if var_translation_direction.get() == 1:                                            # ru-eng
        dictionary = get_dictionary()
    if var_translation_direction.get() == 2:                                            # eng-ru
        dictionary = get_dictionary()
        dictionary = {value: key for key, value in dictionary.items()}
    return dictionary


def get_written_or_voice_method(random_word_for_workout):
    if var_voice_write.get() == 1:                                                      # in write
        random_word_for_workout_label.configure(text=random_word_for_workout)
    if var_voice_write.get() == 2:                                                      # orally
        random_word_for_workout_label.configure(text="")
        get_sound()


def start_workout_choice():
    clean_fields()
    dictionary = get_dictionary_by_translation_direction()

    if dictionary == {}:
        messagebox.showerror(title='Empty set', message='Empty set! Choice other set!')
    else:
        random_word_for_workout = random.choice(list(dictionary))
        correct_translate_word = dictionary.get(random_word_for_workout)
        correct_translate_word_label.configure(text=correct_translate_word)

        if var_translation_direction.get() == 1:                                        # ru-eng
            word_for_sound.configure(text=correct_translate_word)
        else:
            word_for_sound.configure(text=random_word_for_workout)

        show_translation_options_on_buttons(dictionary, correct_translate_word, random_word_for_workout)
        get_written_or_voice_method(random_word_for_workout)


def show_translation_options_on_buttons(dictionary, correct_word, random_word_for_workout):
    # correct word on button
    btns = [word1, word2, word3, word4]
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


def get_result_workout_choice(btn):
    try_choice_user_label.configure(text=btn.cget('text'))
    show_result_workout_choice()


def show_result_workout_choice():
    eng = correct_translate_word_label.cget('text')
    word = try_choice_user_label.cget('text')
    if word == eng:
        msg = f"OK, good job! It's      {eng.upper()}"
        show_result_choice_label.configure(text=msg, text_color='green')
    else:
        msg = f"Fail, correct:     {random_word_for_workout_label.cget('text')} - {eng.upper()}"
        show_result_choice_label.configure(text=msg, text_color='red')


frame_workout_choice = ctk.CTkFrame(tab_choice)
frame_workout_choice.pack(pady=10)
ctk.CTkLabel(frame_workout_choice, text='Choose the workout settings:', font=('Areal', 20)).pack(pady=(10, 0))

frame_option_workout_choice = ctk.CTkFrame(frame_workout_choice)
frame_option_workout_choice.pack(padx=(20, 20), pady=(5, 5))
var_voice_write = IntVar()
var_voice_write.set(1)
written = ctk.CTkRadioButton(frame_option_workout_choice, text='in written', variable=var_voice_write, value=1)
written.grid(row=0, column=0, padx=(10, 10), pady=(5, 5))
orally = ctk.CTkRadioButton(frame_option_workout_choice, text='orally', variable=var_voice_write, value=2)
orally.grid(row=1, column=0, padx=(10, 10), pady=(5, 5))
word_for_sound = ctk.CTkLabel(frame_option_workout_choice, text='1')
var_translation_direction = IntVar()
var_translation_direction.set(1)
ru_eng = ctk.CTkRadioButton(frame_option_workout_choice, text='ru-eng', variable=var_translation_direction, value=1)
ru_eng.grid(row=0, column=1, padx=(10, 10), pady=(5, 5))
eng_ru = ctk.CTkRadioButton(frame_option_workout_choice, text='eng-ru', variable=var_translation_direction, value=2)
eng_ru.grid(row=1, column=1, padx=(10, 10), pady=(5, 5))

correct_translate_word_label = ctk.CTkLabel(frame_workout_choice, text='')
try_choice_user_label = ctk.CTkLabel(frame_workout_choice, text='')

frame_bottom_btn = ctk.CTkFrame(frame_workout_choice)
frame_bottom_btn.pack(side=BOTTOM, padx=(10, 10), pady=(5, 5))
ctk.CTkButton(frame_bottom_btn, text='Listen', font=('Areal', 18),
              command=get_sound).grid(row=0, column=1, padx=(10, 10), pady=(10, 10))
ctk.CTkButton(frame_bottom_btn, text='New word', font=('Areal', 18),
              command=start_workout_choice).grid(row=0, column=0, padx=(10, 10), pady=(10, 10))

show_result_choice_label = ctk.CTkLabel(frame_workout_choice, text='')
show_result_choice_label.pack(side=BOTTOM, padx=(20, 20))

frame_box_for_choice = ctk.CTkFrame(frame_workout_choice)
frame_box_for_choice.pack()
random_word_for_workout_label = ctk.CTkLabel(frame_box_for_choice, text='',
                                             font=('Areal', 22, 'bold'), text_color='green')
random_word_for_workout_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10)
word1 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                      command=lambda: get_result_workout_choice(word1))
word1.grid(row=1, column=0, padx=10, pady=10)
word2 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                      command=lambda: get_result_workout_choice(word2))
word2.grid(row=2, column=0, padx=10, pady=10)
word3 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                      command=lambda: get_result_workout_choice(word3))
word3.grid(row=1, column=1, padx=10, pady=10)
word4 = ctk.CTkButton(frame_box_for_choice, text='', font=('Areal', 18), width=200, height=40,
                      command=lambda: get_result_workout_choice(word4))
word4.grid(row=2, column=1, padx=10, pady=10)


#----------------------------------STATISTIC----------------------------------------------------------

# получаем статистику по статусам слов
def get_statistics():
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
            if a+b+c != 0:
                a_per = round(a / (a + b + c) * 100)
                b_per = round(b / (a + b + c) * 100)
                c_per = round(c / (a + b + c) * 100)
    new_statistics = f'''
    know - {c} ({c_per}%), 
    repeat - {b} ({b_per}%), 
    don't know - {a} ({a_per}%)'''
    statistic_status.configure(text=new_statistics)


frame_right = ctk.CTkFrame(root)
frame_right.grid(row=0, column=3, pady=15, padx=(0, 15), sticky='n')
frame_statistics = ctk.CTkFrame(frame_right)
frame_statistics.grid(row=0, column=0, pady=15, padx=15, sticky='n')
ctk.CTkLabel(frame_statistics, text='Statistics:',
             font=('Areal', 18, 'bold')).grid(row=0, column=0, padx=(10, 10), pady=(10, 0))
start_text_statistic = '''
    know - 0 (0%), 
    repeat - 0 (0%), 
    don't know - 0 (0%)'''
statistic_status = ctk.CTkLabel(frame_statistics, text=start_text_statistic, font=('Areal', 13), justify=tk.LEFT)
statistic_status.grid(row=1, column=0, pady=(0, 10), padx=(0, 10))
ctk.CTkButton(frame_statistics, text='Update statistics',
              command=get_statistics).grid(row=2, column=0, padx=15, pady=15)


#----------------------------------UPDATE STATUS----------------------------------------------------------
# редактирование статуса слов в сете
def update_status():
    group_set = combo_group.get()
    subgroup_set = combo_subgroup.get()
    set_n = int(combo_set.get())
    new_status = var_status.get()
    with sqlite3.connect('app.db') as db:
        cursor = db.cursor()
        query = """
                    UPDATE dictionary
                    SET status = ?
                    WHERE set_n = ? AND subgroup = ? AND group_part = ? 
                    """
        cursor.execute(query, (new_status, set_n, subgroup_set, group_set))
        messagebox.showinfo(title='Status update', message='Status updated successfully!')


# обнуление всех статусов
def update_status_all():
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


frame_update_status = ctk.CTkFrame(frame_right)
frame_update_status.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky='nesw')
ctk.CTkLabel(frame_update_status, text='Update status:', font=('Areal', 18, 'bold')).pack(padx=(10, 10), pady=(20, 10))
var_status = StringVar()
var_status.set('не знаю')
status_unknow_radio = ctk.CTkRadioButton(frame_update_status, text='не знаю', variable=var_status, value='не знаю')
status_unknow_radio.pack(padx=(10, 10), pady=(5, 5))
status_repeat_radio = ctk.CTkRadioButton(frame_update_status, text='повтор', variable=var_status, value='повтор')
status_repeat_radio.pack(padx=(10, 10), pady=(5, 5))
status_know_radio = ctk.CTkRadioButton(frame_update_status, text='знаю', variable=var_status, value='знаю')
status_know_radio.pack(padx=(10, 10), pady=(5, 5))
ctk.CTkButton(frame_update_status, text='Change status of set',
              command=update_status).pack(padx=(10, 10), pady=(15, 5))
ctk.CTkButton(frame_update_status, text='Full "не знаю"-status',
              command=update_status_all).pack(padx=(10, 10), pady=(5, 15))

#----------------------------------APPEARANCE MODE----------------------------------------------------------

def change_appearance_mode_event(event):
    ctk.set_appearance_mode(event)

frame_appearance_mode = ctk.CTkFrame(frame_right)
frame_appearance_mode.grid(row=2, column=0, columnspan=2, pady=(0, 10), padx=(10, 10), sticky='nesw')

appearance_mode_label = ctk.CTkLabel(frame_appearance_mode, text="Appearance Mode:", anchor="w")
appearance_mode_label.grid(row=0, column=0, padx=20, pady=(10, 0))
appearance_mode_optionemenu = ctk.CTkOptionMenu(frame_appearance_mode, values=["Light", "Dark", "System"],
                                                                           command=change_appearance_mode_event)
appearance_mode_optionemenu.set('Dark')
appearance_mode_optionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))


root.mainloop()


