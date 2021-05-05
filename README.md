## Quick Star

### Customization for Quick Star

#### Job Order

- On Save:
  - Create and Submit Purchase Invoice for expenses with Supplier
  - Create and Submit Journal Entry for expenses with Paid From account
  - Create and Submit Payment Entry for Advcances
  - Set Order fees from item price of Default Order Fees Item in company setting
- On Update:
  - Cancel linked Purchase Invoice/Journal Entry of expense has been deleted
  - Cancel Payment Entry if advance has been deleted
- On Submit:
  - Create Sales Invoice with expenses as items
  - Add Default Order Fees Item for order charge
- Job Order Expense row not editable if reference (PI,JE) already created
- Advance row will not be editable if Payment Entry already created.
- On delete of Expense/Advance prompt user for Confirmation. On Save item will be deleted and linked doc cancelled.

### Install

- Create custom field in Company for Default Order Fees Item. Mandatory, Item link.

#### License

MIT
