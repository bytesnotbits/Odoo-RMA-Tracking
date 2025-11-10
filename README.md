# Odoo-RMA-Tracking
Customization Documentation: On-Demand RMA Return Creation

1. Business Context & Objective (The "Why")
- Problem: The business needs to process "Return to Vendor" (RMA) shipments for items without affecting the product's purchase history reporting. Standard Odoo methods (like using a Purchase Order) incorrectly reduce the "Purchased" quantity statistic on the product form.
- Initial Solution: Creating manual RMA(out) and RMA(in) transfers from the Inventory app solves the reporting problem but creates two disconnected transactions, making it difficult to track which returns are still outstanding.
- Objective: Develop a system that allows a user to optionally create a linked RMA(in) transfer directly from a completed RMA(out) transfer. This system must provide a clear, two-way link between the outgoing and incoming shipments while remaining entirely within the Inventory module to protect purchase reporting integrity.
---
2. Solution Architecture Overview
The solution consists of three core components working together:
1. A Custom Relational Field: A Many2one field is added to the stock.picking model to create a direct database link from one transfer to another.
2. A Server Action: A Python script is created to perform the logic of creating the new RMA(in) transfer, copying the relevant data, and populating the relational link in both directions.
3. A UI Button with Conditional Visibility: A button is added to the stock.picking form view, which calls the Server Action. This button is only visible to the user under specific, logical conditions (e.g., only on a completed RMA(out) that does not already have a return linked).
4. The data field is flagged as read only.
---
3. Granular Component Breakdown & Recreation Steps

Component 3.1: The Relational Field

- Purpose: To create a direct, unbreakable link between the outgoing and incoming RMA transfers.
- Technical Details:
  
  Model: Transfer (stock.picking)
  Field Type: Many2one
  Field Name (Technical): x_studio_related_rma
  Field Label (English): Related RMA
  Related Model: Transfer (stock.picking)
  
- Recreation Steps (Using Studio):
  
  Navigate to any transfer document (Inventory > Operations > Transfers).
  Enter Studio.
  From the "Fields" list on the left, drag a Many2one field onto the form.
  In the field properties, set the "Label" to Related RMA and the "Related Model" to Transfer.
  Note the technical name assigned by Studio (e.g., x_studio_related_rma) for use in the Server Action code.
  Close Studio.
  

Component 3.2: The Server Action (The Logic)

- Purpose: To execute the code that creates and links the return transfer.
- Recreation Steps:
  Navigate to Settings > Technical > Server Actions.
  Click Create.
  Set the Name to Create and Link Return RMA.
  Set the Model to Transfer (stock.picking).
  Set the Action To Do type to Execute Python Code.
  Paste the Python code below into the code editor.
  Click Save.
  Crucially, click the "Create Contextual Action" button after saving. This makes the action available to the UI.

Component 3.3: The UI Button (The Trigger)

- Purpose: To provide a user-friendly, one-click method to run the Server Action.
- Recreation Steps (Using Studio):
  
  Navigate to a transfer document (Inventory > Operations > Transfers) and enter Studio.
  Go to the "Buttons" tab and click "Add a button".
  Configure the button properties:
  
  Button Text: Create Return RMA
  Use Existing Action: Check this box.
  Action: Select the Create and Link Return RMA server action.
  
  
  Configure the "Invisible" attribute with the following domain rules, ensuring the logic is set to "Match any of the following rules:" (OR logic).
  
  Rule 1: [ "Related RMA", "is set" ]
  Rule 2: [ "Operation Type", "is not", "RMA(out)" ]
  Rule 3: [ "Status", "is not", "Done" ]
  
  
  Close Studio to save the view changes.
  
---

Summary Report for Developer

Feature: On-Demand RMA Return Creation
Objective: To create a linked RMA(in) transfer from a validated RMA(out) transfer via a user-controlled button, without affecting the Purchase module.
Components Created:
1. Custom Field (via Studio):
   Model: stock.picking
   Name: x_studio_related_rma
   Type: Many2one
   Relation: stock.picking
   
2. Server Action:
   Name: Create and Link Return RMA
   Model: stock.picking
   Type: Execute Python Code
   Code: [See Python code block above]
   
3. UI Modification (via Studio):
   View Modified: stock.picking form view.
   Element: A new <button> has been added to the header.
   Button Label: Create Return RMA
   Action Called: Create and Link Return RMA (Server Action)
   Visibility Domain (attrs="{'invisible': ...}"): The button is hidden if ANY of the following are true:
   
   x_studio_related_rma is not False.
   picking_type_id.name is not 'RMA(out)'.
   state is not 'done'.
   
   
   Domain String: [ "|", "|", ("x_studio_related_rma", "!=", False), ("picking_type_id.name", "!=", "RMA(out)"), ("state", "!=", "done") ]
