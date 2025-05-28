import pandas as pd
from datetime import datetime
import re
def filter_lines(lines):
    start_index = None
    end_index = None

    # Find start and end indices
    start_index = None
    end_index = None

    for i in range(len(lines)):
       line = lines[i]
       if "INCOME TAX DEPARTMENT" in line and start_index is None:
           start_index = i
       if "Signature" in line:
          end_index = i
          break


    # Filter lines based on conditions
    filtered_lines = []
    if start_index is not None and end_index is not None:
        for line in lines[start_index:end_index + 1]:
            if len(line.strip()) > 2:
                filtered_lines.append(line.strip())
    
    return filtered_lines


# -------------- DEBUGGING ----------------

# Example list of lines
# lines = [
#     "Some irrelevant text",
#     "INCOME TAX DEPARTMENT",
#     "Line with relevant information",
#     "Signature",
#     "More irrelevant text"
# ]

# # Filter lines
# filtered_lines = filter_lines(lines)

# # Print filtered lines
# for line in filtered_lines:
#     print(line)


def create_dataframe(texts):

    lines = filter_lines(texts)
    print("="*20)
    print(lines)
    print("="*20)
    data = []
    name = lines[2].strip()
    father_name = lines[3].strip()
    dob = lines[4].strip()
    for i in range(len(lines)):
        if "Permanent Account Number" in lines[i]:
            pan = lines[i+1].strip()
    data.append({"ID": pan, "Name": name, "Father's Name": father_name, "DOB": dob, "ID Type": "PAN"})
    df = pd.DataFrame(data)
    return df

#-----------DEBUGGING------------------

# text=['8', '8', '3', 'HRT', 'INCOME TAX DEPARTMENT', 'GOVT OF INDIA', 'SUMIT', 'RAM SWARUP', '04/03/1992', 'Permanent Account Number', 'J', 'FZKPS9811P', 'Signature', '1', '2', '8']
# df=create_dataframe(text)
# print(df)


def extract_information(data_string):
    # Split the data string into a list of words based on "|"
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]
    print(words)
    extracted_info = {
        "ID": "",
        "Name": "",
        "Father's Name": "",
        "DOB": "",
        "ID Type": "PAN"
    }

    try:
        name_index = words.index("Name") + 1
        extracted_info["Name"] = words[name_index]

        fathers_name_index = name_index + 2
        extracted_info["Father's Name"] = words[fathers_name_index]

        id_number_index = words.index("Permanent Account Number Card") + 1
        extracted_info["ID"] = words[id_number_index]

        dob_index = None
        for i, word in enumerate(words):
            try:
                datetime.strptime(word, "%d/%m/%Y")
                # if word won't be a datetime , it will raise a  exception of value error and in value error we are continuing that index 
                dob_index = i
                break
            except ValueError:
                continue

        if dob_index is not None:
            extracted_info["DOB"] = datetime.strptime(words[dob_index], "%d/%m/%Y")
            # extracted_info["DOB"] = (dob_datetime.year, dob_datetime.month, dob_datetime.day)
        else:
            print("Error: Date of birth not found.")
    except ValueError:
        print("Error: Some required information is missing or incorrectly formatted.")
    return extracted_info


def extract_information1(data_string):
    # Split the data string into a list of words based on "|"
    updated_data_string = data_string.replace(".", "")
    words = [word.strip() for word in updated_data_string.split("|") if len(word.strip()) > 2]
    # print(words)
    extracted_info = {
        "ID": "",
        "Name": "",
        "Gender": "",
        "DOB": "",
        "ID Type": "AADHAR"
    }

    try:
        name_index = words.index("DOB") - 1
        extracted_info["Name"] = words[name_index]

        gender_index = gender_index = next((i for i, word in enumerate(words) if word.lower() in {"male", "female"}), -1)
        extracted_info["Gender"] = words[gender_index]

        # Define the pattern for "XXXX XXXX XXXX"
        pattern1 =re.compile(r'^\d{4} \d{4} \d{4}$')
        pattern2=re.compile(r'^\d{4}$')

        # Find the index where the pattern matches
        id_number_index1= next((i for i, word in enumerate(words) if pattern1.match(word)), -1)
        id_number_index2= next((i for i, word in enumerate(words) if pattern2.match(word)), -1)
        if id_number_index1!=-1:
            extracted_info["ID"] = words[id_number_index1]
        else:
        #   print(id_number_index2)
          try:
            extracted_info["ID"] = words[id_number_index2] + words[id_number_index2 + 1] + words[id_number_index2 + 2]
          except IndexError:
              print("Not enough words after pattern2 match to form ID")
        


        dob_index = None
        for i, word in enumerate(words):
            try:
                datetime.strptime(word, "%d/%m/%Y")
                # if word won't be a datetime , it will raise a  exception of value error and in value error we are continuing that index 
                dob_index = i
                break
            except ValueError:
                continue

        if dob_index is not None:
            extracted_info["DOB"] = datetime.strptime(words[dob_index], "%d/%m/%Y")
            # extracted_info["DOB"] = (dob_datetime.year, dob_datetime.month, dob_datetime.day)
        else:
            print("Error: Date of birth not found.")
    except ValueError:
        print("Error: Some required information is missing or incorrectly formatted.")
    return extracted_info

# ----------------- DEBUGGING--------------------

# text="|8|8|3|HRT|INCOME TAX DEPARTMENT|GOVT OF INDIA|SUMIT|RAM SWARUP|04/03/1992|Permanent Account Number|J|FZKPS9811P|Signature|1|2|8|"
# text="|INCOME TAX DEPARTMENT|GOVT OF INDIA|Permanent Account Number Card|AFEPU7751H|74|Name|UPENDRA NATH SINGH|Father' s Name|MOTI|3426|01/08/1972|"
# text="|HRT TTT|Government of India|Abhishek Singh|DOB|26/07/2004|5y|Male|4205|9308|7552|"
# extracted_info = extract_information1(text)
# print("Extracted Information:")
# print(extracted_info)

