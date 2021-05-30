# Auto Email Console App
This is an consolve app that create emails for a list of customers based on the template email. This app is build on python language.

## Dependencies

* [json](https://docs.python.org/3/library/json.html#module-json): this library is used to read and save data to json file.
* [argparse](https://docs.python.org/3/library/argparse.html#module-argparse): this library is used to get the value of the arguments when launching the app by command line.
* [os](https://docs.python.org/3/library/os.html?highlight=os#module-os): this library is used to manage the folder and file path when the app is running.
* [pandas](https://pandas.pydata.org/docs/): this library is used to process the data of the customer list as a dataframe.
* [datetime](https://docs.python.org/3/library/datetime.html): this library is used to get the date when the app is run.

## Modules

* `read_json_file (path: str)`: this function takes the path of json file that contains the template email as input, then return the data of the template email in `dict` type.
* `read_csv_file (path: str)`: this function takes the path of csv file that contains the customer list as input, then return the data of customer list as a dataframe.
* `process_template_body (body: str)`: this function will change the place holders' format in body of the template email from **"{{ }}"** to **"{  }"**.
* `filter_customer_list (dataframe: DataFrame)`: this function splits the dataframe into two group, one contains the list of customers who have email address, and other one contains those that not have email address.
* `add_date_to_dataframe (dataframe: DataFrame)`: this function appends the **TODAY** column to the dataframe.
* `get_output_email (customer_list: DataFrame, template_email: dict, path: str)`: this function replaces the informatio of each customers to the place holders in the body of template email, and save the output email to json file.
* `write_to_json (data: dict, paht: str)`: this function saves the output email to json file.
* `get_output_error (customer_list: DataFrame, path: str)`: this funcion saves the list of customers who not have email address to the csv file.

## Process steps

1. Read essential data from files.
2. Change the place holders' format in body of template email.
3. Split list of customers into two group.
4. Merge the information of the customers who have email address with the template body.
5. Build the email into dict and save to json file.
6. Save the list of customers without email address to the csv files.

## Usage
`python send_email.py -tp TEMPLATE_PATH -cp CUSTOMER_PATH [-op OUTPUT_PATH] [-ep ERROR_PATH]`

### Arguments:
* -tp, --template_path: Path to the template email json file. This is required.
* -cp, --customer_path: Path to the customer list csv file. This is required.
* -op, --out_path: Path to the folder that contains the invite emails. This is optional, the defautl folder is **'./output_emails/'**.
* -ep, error_path: Path to the file that cotains the list of customers without email address. This is optinal, the default path is **'./errors.csv'**.

### Example
`python send_email.py -tp template_email.json -cp customers.csv`

## Docker

[Docker image](https://hub.docker.com/r/ledat2110/auto_email)
* `sudo docker pull ledat2110/auto_emal` to pull the docker image from docker hub.
* `sudo docker run -dit --name auto_email ledat2110/auto_email` to run docker container from image.

### Run app by command line
* `sudo docker cp /path/to/template_email.json auto_email:/app/template_email.json` copy template email file from host to container with name **template_email.json**.
* `sudo docker cp /path/to/customers.csv auto_email:/app/customers.csv` copy customers file from host to container with name **customers.csv**.
* `sudo docker exec auto_email python send_email.py` run to generate emails.
* `sudo docker cp auto_email:/app/outut_emails /path/to/output_emails` copy the output emails from container to host.
* `sudo docker cp auto_email:/app/errors.csv /path/to/errors.csv` copy the output errors file from container to host.

### Run app by sh file
After pull the docker image and run the container, put the template email json file and customers csv file in the same folder with sh file **run_docker.sh** with the name **template_email.json** and **customers.csv**, respectively.

`bash run_docker.sh`

The output emails in the **output_emails** folder, and errors file with name **errors.csv**.
