# Enriching Guardium Insights with entitlement information using a CSV file

Entitlements provide granular visibility into things like user entitlements, dormant accounts, and excessive privileges 
in support of governance controls. The following code is tailored for Guardium Data Protection (GDP) entitlement 
exports, but can be adjusted for other vendor outputs. 

Learn more about Guardium entitlements 
[here](https://www.ibm.com/security/digital-assets/guardium/data-protection-demo/data-risks/3.html).

## Instructions

- Install Python package dependencies: 
  - requests
  - csv

- [Create a custom data](https://www.ibm.com/docs/en/guardium-insights/saas?topic=integrations-working-data-sets) set 
within Guardium Insights that exactly match those found within the CSV. To match what is expected by the code and csv 
sample in this repo, use the following definition:
<details>
<summary>Custom data set definition</summary>

dataset_name: `ENTITLEMENT_INFO`

column_name: `Grantee`, column type: `TEXT`, column size: `256`

column_name: `Grantee_Type`, column type: `TEXT`, column size: `256`

column_name: `Granted_Role`, column type: `TEXT`, column size: `256`

column_name: `SqlGuard Timestamp`, column type: `TIMESTAMP`, column size: `10`

column_name: `DB Name`, column type: `TEXT`, column size: `256`

column_name: `Count of Microsoft SQL Server Role Granted To User And Roles`, column type: `INTEGER`, column size: `4`

column_name: `Hostname`, column type: `TEXT`, column size: `256`

column_name: `Service name`, column type: `TEXT`, column size: `256`

column_name: `Server IP`, column type: `TEXT`, column size: `256`

column_name: `Database name`, column type: `TEXT`, column size: `256`

column_name: `Port`, column type: `INTEGER`, column size: `4`

Note: The standard Datasource Details column, which contains multiple attributes, has been broken out into individual 
column names to making joining on the column names easier within Guardium Insights reports (later).

</details>


- [Create an API](https://www.ibm.com/docs/en/guardium-insights/saas?topic=configuring-creating-api-keys) key in Guardium Insights

- Configure the variables within the python script (`gdp_entitlement_gi_enrichment.py`) to use your information:
  - `data_set_name`: The name of the data set you created in Guardium Insights (must be all uppercase)
  - `entitlements_csv_path`: Path to the where the CSV entitlements file is stored
  - `gi_url`: URL for the Guardium Insights instance. For SaaS, it's always https://guardium.security.ibm.com/
  - `api_auth_key`: The encoded token generated from the previous step

- Run `gdp_entitlement_gi_enrichment.py` perform the CSV parse and data set insert.
- Use your custom data set by [joining it with a report](https://www.ibm.com/docs/en/guardium-insights/saas?topic=reports-joining-report-data-custom-data) 
in Guardium Insights. A good starter use case is joining the **Assets** report on *Server IP* and *Database name*. This
will tell you entitlements on a assets basis.