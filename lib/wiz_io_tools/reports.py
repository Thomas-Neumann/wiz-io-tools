#!/usr/bin/env python3

import csv
import logging

from typing import List
from wiz_io_tools.data.issue    import Issue
from wiz_io_tools.data.resource import Resource

def parse_issue_record(record):
    issue = Issue()
    issue.created_at           = record['Created At']
    issue.title                = record['Title']
    issue.severity             = record['Severity']
    issue.status               = record['Status']
    issue.subscription_id      = record['Subscription ID']
    issue.project_ids          = record['Project IDs']
    issue.project_names        = record['Project Names']
    issue.resolved_time        = record['Resolved Time']
    issue.resolution           = record['Resolution']
    issue.control_id           = record['Control ID']
    issue.resource             = parse_resource_record(record)
    issue.issue_id             = record['Issue ID']
    issue.resource_vertex_id   = record['Resource vertex ID']
    issue.ticket_urls          = record['Ticket URLs']
    return issue

def parse_resource_record(record):
    resource = Resource()
    resource.name          = record['Resource Name']
    resource.type          = record['Resource Type']
    resource.external_id   = record['Resource external ID']
    resource.region        = record['Resource Region']
    resource.status        = record['Resource Status']
    resource.platform      = record['Resource Platform']
    resource.os            = record['Resource OS']
    resource.original_json = record['Resource original JSON']
    return resource

def parse_issues_report(csvfile) -> List[Issue]:
    print(f"I: Parsing report '{csvfile}'.")

    with open(csvfile, mode='r', newline='') as fh:
        rh = csv.DictReader(fh, delimiter=',', quotechar='"')
        fieldnames_have = rh.fieldnames
        fieldnames_want = [
            'Created At',
            'Title',
            'Severity',
            'Status',
            'Resource Type',
            'Resource external ID',
            'Subscription ID',
            'Project IDs',
            'Project Names',
            'Resolved Time',
            'Resolution',
            'Control ID',
            'Resource Name',
            'Resource Region',
            'Resource Status',
            'Resource Platform',
            'Resource OS',
            'Resource original JSON',
            'Issue ID',
            'Resource vertex ID',
            'Ticket URLs'
        ]
        if fieldnames_have == fieldnames_want:
            print("I: Data format is correct.")
            issues = list()
            for row in rh:
                #print(row)
                issues.append(parse_issue_record(row))
            return issues
        else:
            raise Exception("Data issue! Provided file does not contain the expected records!")
