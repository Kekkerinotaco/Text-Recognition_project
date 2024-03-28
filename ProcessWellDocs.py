import shutil
import pathlib
import PIL
from PIL import Image
import sys
import os
import time
import pytesseract


def get_current_app_dir():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return application_path


list_of_unopened_files = []
processed_files_counter = 1


def main(folder_path, result_folder_path, textbox, searched_word="",
         save_empty_pictures_status=False, save_txt_status=False, write_unopened_files=True):
    global processed_files_counter
    application_path = get_current_app_dir()
    tesseract_path = os.path.join(application_path, "LocalTesseract", "tesseract.exe")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    n_of_files = get_n_of_files(folder_path)
    start = time.time()
    wells_list = os.listdir(folder_path)
    processed_files_counter = 1
    for well in wells_list:
        well_folder_path = os.path.join(folder_path, well)
        result_well_folder = os.path.join(result_folder_path, well)
        process_well(well_folder_path, result_well_folder, textbox, n_of_files, searched_word,
                     save_empty_pictures_status=save_empty_pictures_status,
                     save_txt_status=save_txt_status)
    duration = time.time() - start
    if write_unopened_files is True:
        write_error_file(result_folder_path)
    print("Finished processing {} files in {} seconds".format(n_of_files, round(duration, 3)))


def get_n_of_files(folder_path):
    n_of_files = 0
    for root, folders, files in os.walk(folder_path):
        for file in files:
            n_of_files += 1
    return n_of_files


def process_well(folder_path, result_folder_path, textbox, n_of_files, searched_word, save_empty_pictures_status,
                 save_txt_status):
    global list_of_unopened_files
    global processed_files_counter
    tag_found_folder = os.path.join(result_folder_path, f"Тег [{searched_word}] найден")
    tag_not_found_folder = os.path.join(result_folder_path, f"Тег [{searched_word}] не найден")
    for root, folders, files in os.walk(folder_path):
        for file in files:
            textbox.delete(index1=0.0, index2=1000.0)
            textbox.insert("insert",
                           "Производится обработка файла {} из {}.\n".format(processed_files_counter, n_of_files))
            textbox.update()
            processed_files_counter += 1
            file_path = os.path.join(root, file)
            try:
                file_content = pytesseract.image_to_string(Image.open(file_path), lang="rus")
                ext = pathlib.Path(file_path).suffix
                if searched_word.upper() in file_content.upper():
                    result_file_path = os.path.join(tag_found_folder, file)
                    manage_folder_existence(result_folder_path)
                    manage_folder_existence(tag_found_folder)
                    shutil.copy(file_path, result_file_path)
                    if save_txt_status == True:
                        txt_file_path = make_text_file_name(tag_found_folder, file, ext)
                        with open(txt_file_path, "w") as txt_file:
                            txt_file.write(file_content)
                else:
                    if save_empty_pictures_status == True:
                        result_file_path = os.path.join(tag_not_found_folder, file)
                        manage_folder_existence(result_folder_path)
                        manage_folder_existence(tag_not_found_folder)
                        shutil.copy(file_path, result_file_path)
                        if save_txt_status == True:
                            txt_file_path = make_text_file_name(tag_not_found_folder, file, ext)
                            with open(txt_file_path, "w") as txt_file:
                                txt_file.write(file_content)
            except PIL.UnidentifiedImageError:
                print("Unable to open image: {}".format(file))
                list_of_unopened_files.append(file_path)


def manage_folder_existence(folder_path):
    """Функция контролирует существование папки по переданному пути"""
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    except NotADirectoryError:
        pass


def make_text_file_name(folder_path, file_name, ext):
    """Функция создает путь для сохранения файла .txt"""
    index = file_name.rfind(ext)
    file_base_name = file_name[:index]
    new_file_path = os.path.join(folder_path, file_base_name + ".txt")
    return new_file_path


def write_error_file(folder_path):
    global list_of_unopened_files
    error_file_path = os.path.join(folder_path, "!.UnopenedFiles.txt")
    if len(list_of_unopened_files) > 0:
        with open(error_file_path, "w") as file:
            for error_file in list_of_unopened_files:
                file.write(error_file)
                file.write("\n")
