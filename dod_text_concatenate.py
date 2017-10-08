import os
import sys


def main():
	text_default_directory = "./dod_parsed_text"
	name_output_file = "step_03_contract_python"

	print("This program will concatenate the dod_parsed_text files into a single file")
# delete empty files
	file_name_list = os.listdir(text_default_directory)
	list_deleted_files = []
	for text_file_name in file_name_list:
		file_path = os.path.join(text_default_directory, text_file_name)
		if os.stat(file_path).st_size == 0:
			os.remove(file_path)
			list_deleted_files.append(text_file_name)
	print(len(list_deleted_files), "empty files deleted")
	file_name_list = [x for x in file_name_list if x not in list_deleted_files]

#Concatenate files
	outputfile = open(name_output_file,"w+")
	with open(name_output_file, "w") as outfile:
		for text_file_name in file_name_list:
			file_path = os.path.join(text_default_directory, text_file_name)
			with open(file_path) as infile:
				for line in infile:
					outfile.write(line)
				outfile.write("\n******************************\n")

	print("Concatenated file saved as: ", name_output_file)

if __name__ == "__main__":
    main()