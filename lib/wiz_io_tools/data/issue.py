#!/usr/bin/env python3
#
# data class for an issue
#

class Issue:
    def __init__(self):
        self.created_at           = ""
        self.title                = ""
        self.severity             = ""
        self.status               = ""
        self.subscription_id      = ""
        self.project_ids          = ""
        self.project_names        = ""
        self.resolved_time        = ""
        self.resolution           = ""
        self.control_id           = ""
        self.resource             = None
        self.issue_id             = ""
        self.resource_vertex_id   = ""
        self.ticket_urls          = ""
