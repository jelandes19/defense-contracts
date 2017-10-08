from bs4 import BeautifulSoup
import os
import sys
import re
import textwrap
try:
    import html5lib
except ModuleNotFoundError as e:
    print("html5lib module needs to be installed for this program to run properly: "+ e)
    sys.exit(1)


def text(file_number, raw_html_directory):
    file_name = str(file_number) + ".html"
    file_path = os.path.join(raw_html_directory, file_name)

    file_handle = open(file_path, "r")
    raw_html = file_handle.read()
    file_handle.close()

#    soup = BeautifulSoup(raw_html, 'html.parser')
    soup = BeautifulSoup(raw_html, 'html5lib') #"html.parser" was not correcting the html code (it wass just ignoring incorrect tags)

# Contract number, date. In the right format "02 25, 2000"  ----> "20000225"
    contract_num = soup.find(id="ctl00_cphBody_ContentContents_PressOpsItemContentPreTitle").get_text().strip("No: ").strip()
    rep = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"} 
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    date_contract = pattern.sub(lambda m: rep[re.escape(m.group(0))], contract_num[6:])
    date_contract = "".join([date_contract[7:], date_contract[:2], date_contract[3:][:2]])
    contract_num = "\n".join([str(file_number), date_contract, contract_num[:6]+"\n"])
# Separating by paragraph s.t. contract_num can be added. Does not write one line paragraphs such as types of contract titles (e.g. NAVY)
# or empty paragraphs created by the parser. 
    raw_text = ""
    paragraph_texts = soup.find(id="ctl00_cphBody_ContentContents_lblArticleContent").find_all("p")
    for paragraph in paragraph_texts:
        if len(paragraph.get_text()) > 70:
            text_paragraph = paragraph.get_text().strip()
            text_paragraph = "\n".join(textwrap.wrap(text_paragraph, width = 90))
            raw_text = raw_text + "\nidentifier_" + text_paragraph
    if len(raw_text) < 50:
        raw_text = ""
        paragraph_texts = soup.find(id="ctl00_cphBody_ContentContents_lblArticleContent").find_all("div")
        for paragraph in paragraph_texts:
            if len(paragraph.get_text()) > 70:
                text_paragraph = paragraph.get_text().strip()
                text_paragraph = "\n".join(textwrap.wrap(text_paragraph, width = 90))
                raw_text = raw_text + "\nidentifier_"  + text_paragraph

    start_index = 0
    end_index = raw_text.find('Most Recent Contracts')
    if end_index == -1:
        end_index = 1000000000
    if start_index == -1:
        return []
    else:
        contracts = raw_text[start_index:end_index].strip()
        contracts = re.sub(r"\nidentifier_", "\n******************************\n"+contract_num, contracts).strip("identifier_")
#        contracts = contracts.replace("\n\n", "\n******************************\n"+contract_num+"\n")
        part = re.compile('(...-..)').split(contract_num)
        part += re.compile('(\(......-..-.-....\))').split(contracts)
        return "".join(part)

        # return raw_text[start_index:end_index].strip().replace('\n\n', 'XXXX').replace('\n', '').replace('XXXX', '\n').split('\n')

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
        try:
            out_lines = text(number, raw_html_directory)
        except UnicodeDecodeError as e:
            print("Error found: ", e)
        out_file = os.path.join(text_directory, str(number) + ".txt")
        print("Writing " + out_file)
        out_file_handle = open(out_file, "w")
        for line in out_lines:
                out_file_handle.write(line)
        out_file_handle.close()

if __name__ == "__main__":
    main()
