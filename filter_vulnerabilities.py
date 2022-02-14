#!/usr/bin/env python3
#
# filter out known vulnerabilities from wiz.io vulnerability report
#
# ./filter_vulnerabilities.py <report_file1> [<report_file2> ...]
#
# usage:
#    ./filter_vulnerabilities.py data/vulnerability-reports/1644573599308653316.csv
#    ./filter_vulnerabilities.py file1.csv file2.csv

# input file format:
# Created At,Title,Severity,Status,Resource Type,Resource external ID,Subscription ID,Project IDs,Project Names,Resolved Time,Resolution,Control ID,Resource Name,Resource Region,Resource Status,Resource Platform,Resource OS,Resource original JSON,Issue ID,Resource vertex ID,Ticket URLs

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__) + "/lib")

import wiz_io_tools.reports

from wiz_io_tools.reports_cli import configure_logger, parse_argv

# version string including prerelease and metadata (if appliccable)
# major.minor.patch[-prerelease][+metadata]
VERSIONSTRING="0.1.0-alpha2"

LH = logging.getLogger()

if __name__ == "__main__":
    configure_logger(LH, logging.INFO)

    config = parse_argv(VERSIONSTRING)

    ignored_issues = [
        # [ issue.title, issue.resource.external_id ]
    ]
    fixed_issues = [
        # [ issue.title, issue.resource.external_id ]
    ]
    exemptions = [
        # [ issue.title, issue.resource.external_id ]
    ]

    error_count = 0

    issues = list()
    for csvfile in config["reports"]:
        try:
            issues.extend(wiz_io_tools.reports.parse_issues_report(csvfile))
        except FileNotFoundError as e:
            LH.error("Skipping '%s': %s", csvfile, e.strerror)
            error_count += 1

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

    issue_count = len(issues)
    if issue_count == 0:
        LH.info("Found no issues. Awesome!")
    else:
        if counters_severity["CRITICAL"] == 0 and counters_severity["HIGH"] == 0:
            LH.warning("Found %i issues. (no critical, no high)", issue_count, counters_severity["CRITICAL"], counters_severity["HIGH"])
        else:
            LH.error("Found %i issues. (critical: %i, high: %i)", issue_count, counters_severity["CRITICAL"], counters_severity["HIGH"])
    LH.info("(%i already fixed, %i exempted, %i ignored)", counter_already_fixed, counter_exempted, counter_ignored)
    if error_count:
        LH.warning("Encountered %i error(s)! Please verify input.", error_count)
