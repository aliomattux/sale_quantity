from openerp.osv import osv, fields

class SaleOrderLine(osv.osv):
    _inherit = 'sale.order.line'
    _columns = {
	'immediately_usable_qty': fields.related('product_id', 'immediately_usable_qty', type="float", string="Available Qty"),
#	'potential_qty': fields.related('product_id', 'potential_qty', type="float", string="Build Qty"),

    }


    def product_id_change_with_wh(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, warehouse_id=False, context=None):
        context = context or {}
	print 'Doing Call'
        product_uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        warning = {}
        #UoM False due to hack which makes sure uom changes price, ... in product_id_change
        res = super(SaleOrderLine, self).product_id_change_with_wh(cr, uid, ids, pricelist, product, qty=qty,
            uom=False, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag, warehouse_id=warehouse_id, context=context)

        if not product:
            res['value'].update({'product_packaging': False})
            return res

        # set product uom in context to get virtual stock in current uom
        if 'product_uom' in res.get('value', {}):
            # use the uom changed by super call
            context = dict(context, uom=res['value']['product_uom'])
        elif uom:
            # fallback on selected
            context = dict(context, uom=uom)

        #update of result obtained in super function
	product = product_obj.browse(cr, uid, product, context=context)
	res['value'].update({'immediately_usable_qty': product.immediately_usable_qty})
#		'potential_qty': product.potential_qty})

	return res
