from PIL import Image
import pytesseract
import os
import csv
import re
from datetime import datetime

# Set the path to the tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"/usr/local/bin/tesseract"

def extract_info(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def parse_text(extracted_text):
    placeholder_date = '00-00-0000'
    placeholder_time = '00:00'

    data = {
        'Transaction Type': 'SELL',
        'Date': None,
        'Time': None,
        'Company Name': None,
        'No. of Shares': None,
        'Price per Share USD': None,
    }

    # Regex patterns
    date_time_pattern = re.compile(r'(\d{2} \w{3} \d{4}) G (\d{2}:\d{2})')
    company_name_pattern = re.compile(r'(?<=\n).+(?=\nMarket sell contract note)')
    shares_price_pattern = re.compile(r'(\d+\.\d+)\s*\$(\d+\.\d{2})')

    # Search for patterns in the text
    date_time_match = date_time_pattern.search(extracted_text)
    if date_time_match:
        data['Date'] = date_time_match.group(1)
        data['Time'] = date_time_match.group(2)

    company_name_match = company_name_pattern.search(extracted_text)
    if company_name_match:
        data['Company Name'] = company_name_match.group().strip()

    shares_price_match = shares_price_pattern.search(extracted_text)
    if shares_price_match:
        data['No. of Shares'] = shares_price_match.group(1)
        data['Price per Share USD'] = '$' + shares_price_match.group(2)

    
    # If the date is missing, set it to the placeholder
    if not data['Date']:
        data['Date'] = placeholder_date
    else:
        # Convert date from 'DD MMM YYYY' to 'DD-MM-YYYY'
        date_obj = datetime.strptime(data['Date'], '%d %b %Y')
        data['Date'] = date_obj.strftime('%d-%m-%Y')

    # If the time is missing, set it to the placeholder
    if not data['Time']:
        data['Time'] = placeholder_time

    return data  # Continue to return a dictionary

def check_duplicate(csv_filename, new_data):
    with open(csv_filename, 'r', newline='') as file:
        existing_data = list(csv.reader(file))
        # Skip the header row and check if there is any data to compare against
        if len(existing_data) > 1:
            new_data_list = [
                new_data['Transaction Type'],
                new_data['Date'],
                new_data['Time'],
                new_data['Company Name'],
                new_data['No. of Shares'],
                new_data['Price per Share USD'],
            ]
            for row in existing_data[1:]:
                # If the row matches and all values are not None or placeholders, consider it a duplicate
                if row == new_data_list and not any(v in [None, '00-00-0000', '00:00'] for v in new_data_list):
                    return True
    return False

def parse_and_save(data, csv_filename, image_filename):
    if not check_duplicate(csv_filename, data):
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                data['Transaction Type'],
                data['Date'],
                data['Time'],
                data['Company Name'],
                data['No. of Shares'],
                data['Price per Share USD'],
                image_filename,
            ])

def sort_csv(csv_filename):
    with open(csv_filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    placeholder_date = '00-00-0000'
    placeholder_time = '00:00'

    sorted_data = sorted(
        rows,
        key=lambda row: (
            datetime.strptime(row['Date'], '%d-%m-%Y') if row['Date'] != placeholder_date else datetime.min,
            row['Time'] if row['Time'] != placeholder_time else ''
        )
    )

    with open(csv_filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)


# Function to process a folder of images
def process_folder(folder_path, csv_filename):
    if not os.path.isfile(csv_filename):
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Transaction Type', 'Date', 'Time', 'Company Name', 'No. of Shares', 'Price per Share USD', 'Image Filename'
            ])

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpeg', '.jpg', '.png')):
            print(f"Processing {filename}")
            image_path = os.path.join(folder_path, filename)
            extracted_text = extract_info(image_path)
            data = parse_text(extracted_text)
            if not check_duplicate(csv_filename, data):
                parse_and_save(data, csv_filename, filename)

    sort_csv(csv_filename)


# Example usage
folder_path = '/Users/ethansmith/Documents/GitHub/investments/screenshots/SELL'
csv_filename = '/Users/ethansmith/Documents/GitHub/investments/investment_data_sell.csv'
process_folder(folder_path, csv_filename)