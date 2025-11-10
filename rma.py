# This action runs on the selected 'records' (in this case, just one RMA(out) transfer).
# This action runs on the selected 'records' (in this case, just one RMA(out) transfer).

# The 'record' variable is the transfer where the user clicked the button.

for record in records:
  # --- SAFETY CHECK: Prevent creating a duplicate return ---
  if record.x_studio_related_rma:
  raise UserError("A related RMA has already been created for this transfer.")

# 1. Find the "RMA(in)" Operation Type.
  rma_in_type = env['stock.picking.type'].search([('name', '=', 'RMA(in)')], limit=1)
  if not rma_in_type:
      raise UserError("The 'RMA(in)' Operation Type could not be found. Please check its name.")
  
# 2. Prepare the values for the new RMA(in) transfer.
  new_picking_vals = {
      'picking_type_id': rma_in_type.id,
      'partner_id': record.partner_id.id,
      'origin': record.origin or record.name,
      'move_line_ids_without_package': [], # Using the correct field for creating lines
  }
  
  # 3. Prepare the product lines for the RMA(in).
  for move in record.move_line_ids:
      new_move_vals = {
          'product_id': move.product_id.id,
          'product_uom_id': move.product_uom_id.id,
          'qty_done': move.qty_done, # Using 'qty_done' which is the modern field name
          'location_id': rma_in_type.default_location_src_id.id,
          'location_dest_id': rma_in_type.default_location_dest_id.id,
      }
      new_picking_vals['move_line_ids_without_package'].append((0, 0, new_move_vals))
  
  # 4. Create the new RMA(in) transfer.
  new_picking = env['stock.picking'].create(new_picking_vals)
  
  # 5. Create the two-way link.
  if new_picking:
      record.write({'x_studio_related_rma': new_picking.id})
      new_picking.write({'x_studio_related_rma': record.id})
