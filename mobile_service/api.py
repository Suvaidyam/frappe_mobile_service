import frappe
@frappe.whitelist(allow_guest=True)
def get_meta():
    # print(frappe.get_roles())
    role = f"'Surveyor'"
    sql = f"""
        select
            perm.parent as name,
            perm.read,
            perm.write,
            perm.create,
            perm.delete
        from
            `tabDocPerm` as perm
        where
            perm.role = {role} and (perm.write = 1 or perm.create = 1);
    """
    doctypes = frappe.db.sql(sql, as_dict=True)
    for doctype in doctypes:
        meta = frappe.get_meta(doctype.name)
        doctype['fields'] = meta.fields
    return doctypes
