
# csvAppSegExportZPA

This tool helps in taking all the application segments in your ZPA and saves it in CSV format.


# Use Case

This tool is developed to help administrators to export a copy of all application segments published in Zscaler Private Access.

# Installation

Requirements for installation:

    1. pip3 install requests
    2. ZPA API Key
    3. ZPA Customer ID



## Environment Variables, ZPA Tenant, and ZPA Customer ID

To run this project, you will need to add the following environment variables to your .env file or to your ~/.profile.

`export ZPA_CL_ID='Zscaler Client ID'`

`export ZPA_SC='Zscaler Secret Key'`

Replace the tenant and customer id.
```python
base_path = "https://config.beta.zscaler.com"
customer_id = "72064120XXXXXXXXX"
```


## Usage/Examples
```bash
git clone git@github.com:meliodaaf/csvAppSegExportZPA.git
```
```python
./appsegments.py
```
#### Sample run. As you can see, it does support pagination. This helps when you organization has a lot of application segments published.
```bash
[*] Authentication successful!
[*] Retrieving apps from page 1.
[*] Retrieving apps from page 2.
[*] Retrieving apps from page 3.
[*] Retrieving apps from page 4.
[*] Retrieving apps from page 5.
[*] Retrieving apps from page 6.
[*] Retrieving apps from page 7.
Reached last page.
```
#### After successful run, CSV file should be generated.
## API Reference

#### Get all items

```http
  GET /mgmtconfig/v1/admin/customers/{customerId}/application
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Pagination

```http
  GET /mgmtconfig/v1/admin/customers/{customerId}/application?page=1&pagesize=500
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `page`      | `string` | `Default value: 1`              |
| `pagesize` | `string` | `Value is up to 500`|

## Roadmap

    1. Add export for Policies
    2. Correlate Application Segments and Policies

#### Links:

[ZPA API Reference](https://help.zscaler.com/zpa/application-segment-use-cases)

