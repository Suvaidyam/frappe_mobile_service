import frappe
import copy
import pickle
fields_keys = [
    'name', 'fieldname','fieldtype',
    'label', 'options','mandatory_depends_on',
    'read_only_depends_on','depends_on','read_only',
    'length','not_nullable','is_virtual','non_negative',
    'in_list_view','in_filter','description','default',
    'unique','reqd'
]
@frappe.whitelist(allow_guest=True)
def get_meta(doctype=None):
    # print(frappe.get_roles())
    args = frappe.request.args
    doctype = args.get('doctype', None)
    role = f"'Surveyor'"
    _doctype = ""
    if doctype:
        _doctype = f"perm.parent='{doctype}' AND "
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
            {_doctype} perm.role = {role} and (perm.write = 1 or perm.create = 1);
    """
    # print(sql)
    doctypes = frappe.db.sql(sql, as_dict=True)
    for dt in doctypes:
        meta = frappe.get_meta(dt.name)
        property_setters = frappe.db.get_values(
            "Property Setter",
            filters={"doc_type": dt.name},
            fieldname="field_name,property,value",
            as_dict=True,
        )
        props = {}
        for prop in property_setters:
            props[prop.get('field_name')] = prop
        fields = []
        for field in meta.fields:
            if field.get('hidden') != 1:
                keys = [k for k in field.__dict__.keys() if k in fields_keys]
                fld = {}
                for k in keys:
                    fld[k] = field.get(k)
                    if props.get(field.fieldname, None):
                        prp = props.get(field.fieldname)
                        fld[prp.get('property')] = prp.get('value')
                fields.append(fld)
        dt['fields'] = fields
    return doctypes
