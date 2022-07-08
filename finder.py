#!/usr/bin/python3

import csv
import argparse


parser = argparse.ArgumentParser(description="ZIA Automation Tool for creating and updating URL categories.")
parser.add_argument("--app", "-a", required=True, help="Target application")
args = parser.parse_args()
app = args.app

def main():
    appseeker(app)
    

def appseeker(app):
    
    with open("application_segments.csv", "r") as handle:
        file = csv.DictReader(handle)

        for item in file:
            name = item["Application Segment"]
            tports = item["TCP Ports"]
            uports = item["UDP Ports"]
            server_group = item["Server Groups"]
            domains = item["Domain Names"]
            segment_group = item["Segment Group"]
            if app in domains:  
                print("\n" + "-" * 50)
                print("Application Segment: " + name)
                print("Domains: " + domains)
                print("Segment Group: " + segment_group)
                if tports:
                    print("TCP Ports: " + tports)
                if uports:
                    print("UDP Ports: " + uports)
                print("Server Groups: " + server_group)
                policyseeker(segment_group)

def policyseeker(segment_group):

    with open("global_policies.csv", "r") as handle:
        file = csv.DictReader(handle)

        for item in file:
            name = item["Rule Name"]
            segment_name = item["Segment Groups"]
            ad_group = item["AD Groups"]
            segment_groups = item["Segment Groups"]
            idp = item["IDP"]
            machine_group = item["Machine Groups"]
            posture = item["Posture"]
            if segment_group in segment_groups:
                print("\nRule Name: " + name)
                print("Segment Groups: " + segment_name)
                if ad_group != "[]":
                    print("AD Groups: " + ad_group)
                if idp != "[]":
                    print("IDP: " + idp)
                if machine_group != "[]":
                    print("Machine Group: " + machine_group)
                if posture != "[]":
                    print("Posture: " + posture)
                

if __name__ == "__main__": main()
