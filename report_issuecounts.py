#!/usr/bin/env python3
"""
show issue counters for all accounts you have access to

sample output:

  account name         critical     high   medium      low
  ---------------------------------------------------------
  aws-account1-npn           27       85      555      292
  aws-account2                4       92      392      132

usage:
  ./report_issuecounts.py --oauth-token="ey...kA"
"""

import argparse
import os
import requests
import sys

sys.path.insert(0, os.path.dirname(__file__) + "/lib")

import oauth

# version string including prerelease and metadata (if appliccable)
# major.minor.patch[-prerelease][+metadata]
VERSIONSTRING="0.1.0-alpha1"


# reusable functions
def query_wiz_api(token, query, variables):
  """
  query WIZ API for the given query data schema
  """

  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
  }

  data = {"variables": variables, "query": query}

  try:
      result = requests.post(url="https://api.us8.app.wiz.io/graphql", json=data, headers=headers)

  except Exception as e:
      if '502: Bad Gateway' not in str(e) and '503: Service Unavailable' not in str(e):
          print(f"Wiz-API-Error: {str(e)}")
          return(e)
      else:
          print("Retry")

  return result.json()


def get_issuecounts(oauth_token):
    query = (
        """
        query CloudAccounts($first: Int, $cloudAccountFilter: CloudAccountFilters, $issueFilter: IssueFilters) {
            cloudAccounts(first: $first, filterBy: $cloudAccountFilter) {
                nodes {
                    accountName: name
                    provider: cloudProvider
                    status
                    lastScan: lastScannedAt
                    resources: resourceCount
                    issues(filterBy: $issueFilter) {
                        info: informationalSeverityCount
                        low: lowSeverityCount
                        medium: mediumSeverityCount
                        high: highSeverityCount
                        critical: criticalSeverityCount
                    }
                }
            }
        }
        """
    )
    variables = {
        "first": 100,
        "cloudAccountFilter": {"status": ["CONNECTED", "PARTIALLY_CONNECTED"]},
        "issueFilter": {"status": ["OPEN", "IN_PROGRESS"]}
    }
    # {
    #     'data': {
    #         'cloudAccounts': {
    #             'nodes': [
    #                 {
    #                     'accountName': 'aws-account1-npn',
    #                     'provider': 'AWS',
    #                     'status': 'CONNECTED',
    #                     'lastScan': '2022-04-04T04:28:27Z',
    #                     'resources': 6025,
    #                     'issues': {
    #                         'info': 0,
    #                         'low': 292,
    #                         'medium': 555,
    #                         'high': 85,
    #                         'critical': 27
    #                     }
    #                 },
    #                 ...
    #             ]
    #         }
    #     }
    # }
    response = query_wiz_api(oauth_token, query, variables)
    return response['data']['cloudAccounts']['nodes']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='get wiz.io vulnerability reports', allow_abbrev=False)
    parser.add_argument('--version', action='version', version=f"%(prog)s v{VERSIONSTRING}")
    parser.add_argument('--oauth-token', dest='oauth_token', type=str, help='provide your wiz.io API OAuth Token')
    args = parser.parse_args()

    oauth_token = None
    if args.oauth_token:
        oauth_token = args.oauth_token
    else:
        url = "https://auth.wiz.io/oauth/token"
        oauth_token = oauth.request_oauth_token(url, args.client_id, args.client_secret, 'beyond-api')

    accounts = get_issuecounts(oauth_token)
    print("account name         critical     high   medium      low")
    print("--------------------------------------------------------")
    for account in accounts:
        accountname = account['accountName']
        # {'info': 0, 'low': 292, 'medium': 555, 'high': 85, 'critical': 27}
        issues_low      = account['issues']['low']
        issues_medium   = account['issues']['medium']
        issues_high     = account['issues']['high']
        issues_critical = account['issues']['critical']
        print("{:20} {:8d} {:8d} {:8d} {:8d}".format(accountname, issues_critical, issues_high, issues_medium, issues_low))
