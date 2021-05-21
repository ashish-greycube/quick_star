// Copyright (c) 2021, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Order", {
  setup: function (frm) {
    $(frm.wrapper).on("grid-row-render", function (e, grid_row) {
      frm.events.disable_row_edit(grid_row);
    });
  },

  job_order_expenses_on_form_rendered: function (frm) {
    frm.events.disable_row_edit(frm.open_grid_row());
  },

  disable_row_edit: function (grid_row) {
    if (
      in_list(
        ["job_order_expenses", "job_order_customer_advance"],
        grid_row.grid.df.fieldname
      )
    ) {
      let can_edit = !grid_row.doc.reference;
      grid_row.activate();
      grid_row.docfields.forEach((f) => {
        grid_row.toggle_editable(
          f.fieldname,
          f.fieldname == "billing_amount" ? true : can_edit
        );
      });
    }
  },

  // validate: function (frm) {
  //   advances = frm.doc.job_order_customer_advance.filter((t) => !t.reference);
  //   // if (!advances.length) return;
  // },
});

frappe.ui.form.on("Job Order Customer Advance", {
  before_job_order_customer_advance_remove: function (frm, cdt, cdn) {
    let delete_doc = frm.doc.job_order_customer_advance.filter(
      (t) => t.name == cdn
    )[0];

    let link = frappe.utils.get_form_link(
      "Payment Entry",
      delete_doc.reference,
      true
    );

    frappe.confirm(
      __("Do you want to cancel Payment Entry {0} linked to this advance.", [
        link,
      ]),
      function () {
        frappe.call({
          method: "delete_advance",
          doc: frm.doc,
          args: {
            doctype: "Payment Entry",
            docname: delete_doc.reference,
          },
          callback: function () {
            frm.reload_doc();
          },
        });
      },
      function () {
        frm.reload_doc();
      }
    );
  },
});

frappe.ui.form.on("Job Order Expenses", {
  before_job_order_expenses_remove: function (frm, cdt, cdn) {
    let delete_doc = frm.doc.job_order_expenses.filter((t) => t.name == cdn)[0];

    let link = frappe.utils.get_form_link(
      delete_doc.reference_doc,
      delete_doc.reference,
      true
    );

    frappe.confirm(
      __("Do you want to cancel {0} {1} linked to this expense.", [
        delete_doc.reference_doc.bold(),
        link,
      ]),
      function () {
        frappe.call({
          method: "delete_expense",
          doc: frm.doc,
          args: {
            doctype: delete_doc.reference_doc,
            docname: delete_doc.reference,
          },
          callback: function () {
            frm.reload_doc();
          },
        });
      },
      function () {
        frm.reload_doc();
      }
    );
  },
});
