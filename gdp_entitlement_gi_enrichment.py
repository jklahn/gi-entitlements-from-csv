import requests
import csv

# Name of the destination data set within Guardium Insights
data_set_name = "ENTITLEMENT_INFO"

# Path to the CSV file for entitlements
entitlements_csv_path = "Microsoft SQL Server Role Granted To User And Role.csv"

# URL to the Guardium Insights instance. For SaaS it's always https://guardium.security.ibm.com/
gi_url = "https://guardium.security.ibm.com/"

# API auth key "Basic...." Best practice is to vault this key and retrieve with it with something like 'keyring'
api_auth_key = "YOUR API KEY HERE"


def create_json_entries_from_csv(path_to_csv_file):
    """Creates entries in a JSON format based on the CSV file import of GDP entitlement information

    Args:
        path_to_csv_file: CSV file that contains an export of entitlement information

    Returns:
        A list of entries (as JSON) to be inserted via API into a custom data set
    """

    with open(path_to_csv_file, newline='', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)  # import the csv file as a dictionary, use headers as key
        entries_list = []

        # loop through the rows in the CSV file
        for row in reader:

            # Get Datasource Details value and split it up by semicolon, remove blank spaces
            data_source_details_split_list = [x.strip() for x in row['Datasource Details'].split(':')]

            # Remove the empty value produced by having two semicolons together
            cleaned_data_source_details_split_list = list(filter(None, data_source_details_split_list))

            # Make all the values in the list lowercase, so it's easier to join with GI reports later
            cleaned_data_source_details_split_list = list(map(lambda x: x.lower(),
                                                              cleaned_data_source_details_split_list))

            # remove old Datasource details from the row JSON
            row.pop('Datasource Details', None)

            # add split out Datasource details as new columns and values
            row.update({'Hostname': cleaned_data_source_details_split_list[0],
                        'Service name':  cleaned_data_source_details_split_list[1],
                        'Server IP':  cleaned_data_source_details_split_list[2],
                        'Database name':  cleaned_data_source_details_split_list[3],
                        'Port':  cleaned_data_source_details_split_list[4]})

            entry_row_json = {'entry': row}     # make the entry

            entries_list.append(entry_row_json)     # add to the list of entries to be added later via REST API

    return entries_list


def add_entries_to_data_set(entries_json, dest_data_set_name, authkey, gi_host_url):
    """Adds entries to a given data set in Guardium Insights via a REST API POST
    NOTE: API limits inserts to 1K entries per request
    TODO: Check for 1K entries limit and loop through POST requests (waiting for success) if necessary
    TODO: Error handling

    Args:
        entries_json: A list of numerical values.
        dest_data_set_name: Name of the data set in Guardium Insights; Must be all uppercase.
        authkey: API authorization key to be used in the request header
        gi_host_url: URL to access the Guardium Insights instance

    Returns:
        The API response as text
    """

    # https://guardium.security.ibm.com/api/v3/integrations/datasets/DATA_SET_NAME
    data_set_api_url = gi_host_url + "api/v3/integrations/datasets/" + dest_data_set_name

    payload = {
        "dataset_name": dest_data_set_name,
        "entries": entries_json
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": authkey
    }

    response = requests.post(data_set_api_url, json=payload, headers=headers, verify=False)

    return response.text


if __name__ == '__main__':    # code to execute if called from command-line

    entries = create_json_entries_from_csv(entitlements_csv_path)

    api_response = add_entries_to_data_set(entries, data_set_name, api_auth_key, gi_url)

    print(api_response)

