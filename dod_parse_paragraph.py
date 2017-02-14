from bs4 import BeautifulSoup
import os
import sys

def text(file_number, raw_html_directory):
    file_name = str(file_number) + ".html"
    file_path = os.path.join(raw_html_directory, file_name)

    file_handle = open(file_path, "r")
    raw_html = file_handle.read()
    file_handle.close()

    soup = BeautifulSoup(raw_html, 'html.parser')
    raw_text = soup.get_text()
    start_index = raw_text.find('CONTRACTS')
    end_index = raw_text.find('Most Recent Contracts')
    if end_index == -1:
        end_index = 1000000000

    if start_index == -1:
        return []
    else:
        return raw_text[start_index:end_index].strip().replace('\n\n', 'XXXX').replace('\n', '').replace('XXXX', '\n').split('\n')

def main():
    raw_html_default_directory = "./dod_raw_html"
    text_default_directory = "./dod_parsed_text"

    print("This program will parse the raw html files of DoD contracts.")
    print("Enter to directory to read the html files from (Press <Enter> for default: \"" + raw_html_default_directory + "\")")
    print(">>> ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()

    if len(line.strip()) > 0:
        raw_html_directory = line.strip()
    else:
        raw_html_directory = raw_html_default_directory

    if not os.path.isdir(raw_html_directory):
        print(raw_html_directory + " does not exist")
        return

    print("Enter to directory to store parsed files (Press <Enter> for default: \"" + text_default_directory + "\")")
    print(">>> ", end="")
    sys.stdout.flush()
    line = sys.stdin.readline()

    if len(line.strip()) > 0:
        text_directory = line.strip()
    else:
        text_directory = text_default_directory 

    if not os.path.isdir(text_directory):
        os.makedirs(text_directory)

    print("raw_html_directory == " + raw_html_directory)
    print("text_directory == " + text_directory)

    file_numbers = []
    for html_file_name in os.listdir(raw_html_directory):
        file_number = html_file_name[:-5]
        file_numbers.append(int(file_number))

    for number in sorted(file_numbers):
        out_lines = text(number, raw_html_directory)
        out_file = os.path.join(text_directory, str(number) + ".txt")
        print("Writing " + out_file)
        out_file_handle = open(out_file, "w")
        for line in out_lines:
            out_file_handle.write(line)
        out_file_handle.close()

if __name__ == "__main__":
    main()
