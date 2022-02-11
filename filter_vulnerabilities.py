#!/usr/bin/env python3
#
# filter out known vulnerabilities from wiz.io vulnerability report
#
# !! this code is an early prototype - it's functional but rough !!
#


# input file format:
# Created At,Title,Severity,Status,Resource Type,Resource external ID,Subscription ID,Project IDs,Project Names,Resolved Time,Resolution,Control ID,Resource Name,Resource Region,Resource Status,Resource Platform,Resource OS,Resource original JSON,Issue ID,Resource vertex ID,Ticket URLs

import os
import sys

sys.path.insert(0, os.path.dirname(__file__) + "/lib")

import wiz_io_tools.reports


if __name__ == "__main__":
    # FIXME provide value via command line
    csvfile = "data/vulnerability-reports/<filename>.csv"

    ignored_issues = [
        # [ issue.title, issue.resource.external_id ]
    ]
    fixed_issues = [
        # [ issue.title, issue.resource.external_id ]
    ]
    exemptions = [
        # [ issue.title, issue.resource.external_id ]
    ]

    issues = wiz_io_tools.reports.parse_issues_report(csvfile)
    counter_ignored       = 0
    counter_already_fixed = 0
    counter_exempted      = 0
    counters_severity = {
        "LOW":      0,
        "MEDIUM":   0,
        "HIGH":     0,
        "CRITICAL": 0,
    }
    for issue in issues:
        counters_severity[issue.severity] += 1
        if issue.severity in ["LOW", "MEDIUM"]:
            continue
        skip_issue = False
        for ignored_issue in ignored_issues:
            if issue.title == ignored_issue[0] and issue.resource.external_id == ignored_issue[1]:
                counter_ignored += 1
                skip_issue = True
                break
        for exemption in exemptions:
            if issue.title == exemption[0] and issue.resource.external_id == exemption[1]:
                counter_exempted += 1
                skip_issue = True
                break
        for fixed_issue in fixed_issues:
            if issue.title == fixed_issue[0] and issue.resource.external_id == fixed_issue[1]:
                counter_already_fixed += 1
                skip_issue = True
                break
        if skip_issue:
            continue

        # add additional filter conditions here

        print("{:100s} {} {} {} <{}>".format(issue.title, issue.severity, issue.resource.name, issue.resource.type, issue.resource.external_id))

    print("Found {} issues. (critical: {}, high: {})".format(len(issues), counters_severity["CRITICAL"], counters_severity["HIGH"]))
    print(f"({counter_already_fixed} already fixed, {counter_exempted} exempted, {counter_ignored} ignored)")
