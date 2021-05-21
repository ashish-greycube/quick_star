from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "job_order",
        "non_standard_fieldnames": {
            "Sales Invoice": "job_order_cf",
        },
        "transactions": [
            {
                "label": _("Sales"),
                "items": [
                    "Sales Invoice",
                ],
            },
        ],
    }
