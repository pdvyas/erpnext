import webnotes
import json

def execute():
	"""replace item_tax_rate stored as string with a json string"""
	webnotes.conn.auto_commit_on_many_writes = 1
	for dt in ["Quotation Item", "Sales Order Item", "Sales Invoice Item", 
			"Delivery Note Item", "Supplier Quotation Item", "Purchase Order Item",
			"Purchase Invoice Item", "Purchase Receipt Item"]:
		print dt
		for d in webnotes.conn.sql("""select name, item_tax_rate from `tab%s`
				where ifnull(item_tax_rate, '')!=''""" % (dt,), as_dict=1):
			try:
				json.loads(d["item_tax_rate"])
			except ValueError, e:
				print "error", d["name"]
				webnotes.conn.sql("""update `tab%s` set item_tax_rate=%s
					where name=%s""" % (dt, "%s", "%s"),
					(json.dumps(eval(d["item_tax_rate"])), d["name"]))
		
	webnotes.conn.auto_commit_on_many_writes = 0