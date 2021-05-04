# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    """Add custom field in Company"""
    custom_fields = {
        "Company": [
            {
                "fieldname": "default_item_for_order_fees_cf",
                "label": "Default Order Fees Item",
                "fieldtype": "Link",
                "insert_after": "default_warehouse_for_sales_return",
                "options": "Item",
            },
        ]
    }
    create_custom_fields(custom_fields, update=False)
