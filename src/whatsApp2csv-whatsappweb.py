import csv
# import tkinter as tk
# from tkinter import filedialog

def whatapp2csv(input_file_path):
    if not input_file_path:
        print("No input file selected. Exiting.")
        exit()

    # Open the input and output files
    with open(input_file_path, "r", encoding="utf-8") as infile:
        # Create list
        csv_writer = []

        # Initialize variables to track message attributes
        current_date = ""
        current_time = ""
        current_name = ""
        current_message = ""
        is_deleted = False
        attachment = ""

        # Iterate through the lines in the input file
        for line in infile:
            line = line.strip()
            line = line.replace(u'\u200e', '') #replace unicode trash character
            current_message = line

            # Check if the line starts with a date and time
            if line.startswith("["):
                datetime_info = line[1 : line.find("]")]
                current_date, current_time = datetime_info.split(", ")

                # Check for a name and message
                name_message = line[line.find("] ") + 2 :]
                if ": " in name_message:
                    current_name, current_message = name_message.split(": ", 1)
                    is_deleted = False
                else:
                    current_name = ""
                    current_message = name_message
                    is_deleted = True

            # Check for attachments
            if "<attached:" in line:
                attachment = line[line.find("<attached:") + 10 : line.find(">")]

            # Check for the "This message was deleted" text
            if "This message was deleted." in line:
                is_deleted = True
                continue

            if current_message.strip() == '':
                continue

            # Write the data to the CSV file
            csv_writer.append(
                [
                    current_date,
                    current_time,
                    current_name,
                    current_message,
                    attachment,
                    is_deleted,
                ]
            )

    print(f'Conversion complete. Lines converted: {len(csv_writer)}')

    return csv_writer