# voca_practice_full_application
Voca Practice is an application for practice your vocabulary. The application exam your knowledge in a smart way. Giving grades for each one of the words. In that way, the application promise you will practice the words you less familiar with.

Main file (tkinter_gui_app.py) contains 4 Classes:
1. Class MainVocaPractice: define general tkinter frames and geometry of the apps etc...
2. Class Menu - the main frame 
3. Class Practice - frame able the user to practice his vocabulary
4. Class Addwords - frame able the user to add more words to his bucket

App's storage creates in 3 text files.
english_bucket
hebrew_bucket
grades_bucket

functions files (voca_practice.py) contains those functions:
1. check_existing_files_or_create_them
2. check_existing_files_or_create_them
3. validation_before_practice
4. check_if_txt_bucket_exist
5. at_least_five_words_in_bucket
6. practice_word
7. user_answer
8. update_degree
