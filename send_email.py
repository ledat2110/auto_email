import json
import argparse
import pandas as pd
import os

from datetime import date

def read_json_file (path: str):
    assert type(path) == str
    assert ".json" in path
    with open(path) as f:
        template_email = json.load(f)

    return template_email

def read_csv_file (path: str):
    assert type(path) == str
    assert ".csv" in path
    df = pd.read_csv(path)

    return df

def process_template_body (template_body: str):
    assert type(template_body) == str
    str_out = template_body.replace('{{', '{').replace('}}', '}')

    return str_out

def filter_customer_list (dataframe: pd.DataFrame):
    assert type(dataframe) == pd.DataFrame
    valid_email_df = dataframe[dataframe['EMAIL'].isnull() == False]
    invalid_email_df = dataframe[dataframe['EMAIL'].isnull() == True]

    return valid_email_df, invalid_email_df

def add_date_to_dataframe (dataframe: pd.DataFrame):
    assert type(dataframe) == pd.DataFrame
    today = date.today().strftime("%d %B %Y")
    dataframe['TODAY'] = today

def write_to_json (data: dict, path: str):
    assert type(data) == dict
    assert type(path) == str
    with open(path, 'w') as f:
        json.dump(data, f)

def get_output_email (customer_list: pd.DataFrame, template_email: dict, path: str):
    assert type(customer_list) == pd.DataFrame
    assert type(template_email) == dict
    assert type(path) == str
    df = customer_list.to_numpy()
    template_body = template_email['body']
    body = []
    email = {}
    email['from'] = template_email['from']
    email['to'] = ''
    email['subject'] = template_email['subject']
    email['mimeType'] = template_email['mimeType']
    email['body'] = ''
    for row in df:
        fname = os.path.join(path, row[3]+'.json')
        email['to'] = row[3]
        email['body'] = template_body.format(TITLE=row[0], FIRST_NAME=row[1], LAST_NAME=row[2], EMAIL=row[3], TODAY=row[4])
        write_to_json(email, fname)

def get_output_error (customer_list: pd.DataFrame, path: str):
    assert type(customer_list) == pd.DataFrame
    assert type(path) == str
    customer_list.to_csv(path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-tp", "--template_path", required=True, help="Path to the template email file")
    parser.add_argument("-cp", "--customer_path", required=True, help="Path to the customer list csv file")
    parser.add_argument("-op", "--output_path", help="Path to the folder that contains the invite emails", default='./output_emails')
    parser.add_argument("-ep", "--error_path", help="Path to the file that contains the list of customers without email", default="./errors.csv")
    args = parser.parse_args()

    # read template_email
    template_email = read_json_file(args.template_path)
    #print(template_email)

    # read customer_list
    customer_list = read_csv_file(args.customer_path)
    #print(customer_list)

    # process template_body
    template_email['body'] = process_template_body(template_email['body'])
    print(template_email)

    # filter customer_list
    valid_email_customers, invalid_email_customers = filter_customer_list(customer_list)
    #print(valid_email_customers)
    #print(invalid_email_customers)

    # get date now
    add_date_to_dataframe(valid_email_customers)
    #print(valid_email_customers)

    # get output email
    get_output_email(valid_email_customers, template_email, args.output_path)

    # get output errors
    get_output_error(invalid_email_customers, args.error_path)
