## Quick Star

### Customization for Quick Star

#### Job Order

- On Save:
  - Create and Submit Purchase Invoice for expenses with Supplier
  - Create and Submit Journal Entry for expenses with Paid From account
  - Create and Submit Payment Entry for Advcances
  - Set Order fees from item price of Default Order Fees Item in company setting
- On Submit:

  - Create Sales Invoice with expenses as items
  - Add Default Order Fees Item for order charge

- Job Order Expense row:

  - not editable if reference (PI,JE) already created
  - Prompt user for confirmation on delete
  - Cancel Purchase Invoice/Journal Entry linked to deleted expense

- Job Order Customer Advance row:

  - Advance row will not be editable if Payment Entry already created.
  - Prompt user for confirmation on delete
  - Cancel Payment Entry linked to deleted advance

### Install

- Create custom field in Company for Default Order Fees Item. Mandatory, Item link.

#### License

MIT
