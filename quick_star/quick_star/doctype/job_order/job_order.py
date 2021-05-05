# -*- coding: utf-8 -*-
# Copyright (c) 2021, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.utils.user_settings import get
from frappe.utils import today, now, flt, get_link_to_form
from erpnext import get_default_currency
from erpnext.stock.get_item_details import get_basic_details
from erpnext.stock.report.item_price_stock.item_price_stock import execute
from erpnext.accounts.doctype.payment_entry.payment_entry import get_party_details
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account


class JobOrder(Document):
    def validate(self):
        self.set_order_fees()
        for d in self.job_order_expenses:
            if not d.reference:
                item_details = get_basic_details(
                    args=frappe._dict(
                        {
                            "item_code": d.item,
                            "company": self.company,
                            "doctype": "Sales Invoice",
                        }
                    ),
                    item=None,
                )
                if d.supplier:
                    self.make_purchase_invoice(d, item_details)
                elif d.paid_from:
                    self.make_journal_entry(d, item_details)

        for d in self.job_order_customer_advance:
            if not d.reference:
                try:
                    pe = self.make_payment_entry(d)
                except Exception as e:
                    raise e

                d.db_set("reference", pe.name)

    def on_update(self):
        pass

    def delete_expense(self, doctype, docname):
        self.job_order_expenses = [
            d for d in self.job_order_expenses if not d.reference == docname
        ]
        self.save()
        frappe.get_doc(doctype, docname).cancel()
        self.reload()

    def delete_advance(
        self,
        docname,
        doctype="Payment Entry",
    ):
        self.job_order_customer_advance = [
            d for d in self.job_order_customer_advance if not d.reference == docname
        ]
        self.save()
        frappe.get_doc(doctype, docname).cancel()
        self.reload()

    def make_payment_entry(self, advance):
        payment = frappe.new_doc("Payment Entry")
        payment.posting_date = today()
        payment.payment_type = "Receive"
        payment.mode_of_payment = advance.mode_of_payment
        payment.party_type = "Customer"
        payment.party = self.customer
        payment.paid_amount = payment.received_amount = abs(advance.amount)
        if advance.cheque_reference:
            payment.reference_no = advance.cheque_reference
            payment.reference_date = advance.posting_date
        out = get_party_details(
            **dict(
                company=self.company,
                party_type="Customer",
                party=self.customer,
                date=today(),
            )
        )
        payment.paid_from = out.get("party_account")
        payment.paid_to = get_bank_cash_account(
            advance.mode_of_payment, self.company
        ).get("account")

        payment.setup_party_account_field()
        payment.set_missing_values()
        payment.save()
        payment.submit()

        return payment

    def make_purchase_invoice(self, item, item_details):
        pi = frappe.new_doc("Purchase Invoice")
        pi.posting_date = today()
        pi.posting_time = now()
        pi.company = self.company
        pi.supplier = item.supplier
        pi.currency = get_default_currency()
        pi.conversion_rate = 1
        pi.taxes_and_charges = item.purchase_taxes_and_charges_template

        pi.append(
            "items",
            {
                "item_code": item.item,
                "rate": item.amount,
                "qty": 1,
                "expense_account": item_details.get("expense_account"),
                "conversion_factor": 1.0,
                "stock_uom": item_details.get("stock_uom"),
            },
        )
        pi.set_taxes()
        pi.calculate_taxes_and_totals()
        pi.insert()
        pi.submit()
        item.db_set("reference_doc", "Purchase Invoice")
        item.db_set("reference", pi.name)

    def make_journal_entry(self, item, item_details):
        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = self.company
        je.remark = "Job Order Entry against: " + self.name
        je.posting_date = today()

        je.append(
            "accounts",
            {
                "account": item.paid_from,
                "credit_in_account_currency": flt(item.amount),
            },
        )

        je.append(
            "accounts",
            {
                "account": item_details.get("expense_account"),
                "debit_in_account_currency": flt(item.amount),
            },
        )

        je.insert()
        je.submit()
        item.db_set("reference_doc", "Journal Entry")
        item.db_set("reference", je.name)

    def set_order_fees(self):
        if not self.order_fees:
            default_order_item = frappe.get_cached_value(
                "Company", self.company, "default_item_for_order_fees_cf"
            )
            if default_order_item:
                _, data = execute(frappe._dict({"item_code": default_order_item}))
                if data:
                    self.order_fees = data[0].get("selling_rate")

    def on_submit(self):
        self.make_sales_invoice()

    def make_sales_invoice(self):
        si = frappe.new_doc("Sales Invoice")
        si.company = self.company
        si.customer = self.customer
        si.currency = frappe.get_cached_value(
            "Company", self.company, "default_currency"
        )
        si.posting_date = today()

        for d in self.job_order_expenses:
            si.append(
                "items", {"item_code": d.item, "rate": d.billing_amount, "qty": 1}
            )
        default_order_item = frappe.get_cached_value(
            "Company", self.company, "default_item_for_order_fees_cf"
        )
        if not default_order_item:
            frappe.throw(
                "Please set the %s in %s Company Settings."
                % (frappe.bold("Default Order Fees Item"), frappe.bold(self.company))
            )
        si.append(
            "items",
            {
                "item_code": default_order_item,
                "rate": self.order_fees,
                "qty": 1,
            },
        )

        si.set_missing_values()
        si.insert()
        # si.submit()
        frappe.msgprint(
            msg=_("Sales Invoice {0} created.").format(
                get_link_to_form("Sales Invoice", si.name)
            ),
            title="Success",
            indicator="green",
        )
