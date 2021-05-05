# -*- coding: utf-8 -*-
from frappe import _
import frappe


def get_data():
    config = [
        {
            "label": _("Documents"),
            "items": [
                {
                    "name": "Job Order",
                    "type": "doctype",
                    "label": _("Job Order"),
                    "description": "Job Order",
                },
            ],
        },
        {
            "label": _("Setup"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Company",
                    "label": "Company",
                    "description": "Company",
                    "condition": frappe.utils.has_common(
                        ["System Manager"], frappe.get_roles()
                    ),
                },
            ],
        },
    ]
    return config
