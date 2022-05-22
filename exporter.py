#!/usr/bin/python3


import json
import os
import requests
import csv

base_path = "https://config.beta.zscaler.com"
customer_id = "72064120240XXXXXXXXXXX"

session = requests.Session()


def main():
    # Main function to execute the functions below.
    access_header = authenticate()
    session.headers.update(access_header)
    application_segments()
    global_policies()
    

def authenticate():
    client_id, client_secret = (os.environ.get("ZPA_CL_ID"), os.environ.get("ZPA_SC"))
    payload = f"client_id={client_id}&client_secret={client_secret}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = session.post(f"{base_path}/signin", data=payload, headers=headers)
    if response.ok:
        print("[*] Authentication successful!")
        token = json.loads(response.text)["access_token"]
        access_header = {
            "Content-type": "application/json", 
            "Authorization": f"Bearer {token}"
            }
        return access_header


def application_segments():
    # Retrieve all application segments.
    output = []
    page = 1
    with open("application_segments.csv", "w") as handle:
        csv_writer = csv.writer(handle)
        
        csv_headers = ["Application Segment", "Domain Names", "Segment Group", "TCP Ports", "UDP Ports", "Server Groups"]
        csv_writer.writerow(csv_headers)
        
        while True:
            try:
                print(f"[*] Retrieving apps from page {page}.")
                params = {"page": page, "pagesize": 500}
                response = session.get(f"{base_path}/mgmtconfig/v1/admin/customers/{customer_id}/application", params=params)
                data = json.loads(response.text)["list"]
                output.extend(data)
                page += 1
            except KeyError:
                print("Reached last page.")
                break
        for item in output:
            try:
                app_name = item["name"]
            except KeyError:
                app_name = None
            try:
                segment_group = item["segmentGroupName"]
            except KeyError:
                segment_group = None
            try:
                tcp_ports = ",".join(list(set(item["tcpPortRanges"])))
            except KeyError:
                tcp_ports = None
            try:
                udp_ports = ",".join(list(set(item["udpPortRanges"])))
            except KeyError:
                udp_ports = None
            try:
                domains = ",".join(item["domainNames"])
            except KeyError:
                domains = None
            try:
                sg = []
                server_groups = item["serverGroups"]
                for index, item in enumerate(server_groups):
                    sg.append(item["name"])
                sg = ",".join(sg)
            except KeyError:
                server_groups = None
                
                
            to_csv = (app_name, domains, segment_group, tcp_ports, udp_ports, sg)
            csv_writer.writerow(to_csv)


def global_policies():
    # Retrieve Global Polocies
    print("[*] Retrieving Global Policies")
    response = session.get(f"{base_path}/mgmtconfig/v1/admin/customers/{customer_id}/policySet/global")
    data = json.loads(response.text)["rules"]
    with open("global_policies.csv", "w") as handler:
        csv_writer = csv.writer(handler)
        headers = ["Rule Order", "Rule Name", "Segment Groups", "AD Groups", "Application Segments", "IDP", "Machine Groups", "Posture"]
        csv_writer.writerow(headers)
        for item in data:
            segment_group = []
            active_directory = []
            apps = []
            client_type = []
            idp = []
            machine_group = []
            posture = []
            name = item["name"]
            rule_order = item["ruleOrder"]
            conditions = item["conditions"]
            for condition in conditions:
                operands = condition["operands"]
                
                for operand in operands:
                    if operand["objectType"] == "APP_GROUP":
                        app = f"Segment group: {operand['name']}"
                        segment_group.append(app)
                    if operand["objectType"] == "SAML":
                        app = f"AD Group: {operand['rhs']}"
                        active_directory.append(app)
                    if operand["objectType"] == "APP":
                        app = f"Application Segments: {operand['name']}"
                        apps.append(app)
                    if operand["objectType"] == "CLIENT_TYPE":
                        app = f"Client Type: {operand['name']}"
                        client_type.append(app)
                    if operand["objectType"] == "IDP":
                        app = f"IDP: {operand['name']}"
                        idp.append(app)
                    if operand["objectType"] == "MACHINE_GRP":
                        app = f"IDP: {operand['name']}"
                        machine_group.append(app)
                    if operand["objectType"] == "POSTURE":
                        app = f"IDP: {operand['name']}"
                        posture.append(app)
            output = rule_order, name, segment_group, active_directory, apps, idp, machine_group, posture
            csv_writer.writerow(output)
                
            


if __name__ == "__main__":
    main()



