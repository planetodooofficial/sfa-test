import base64

from odoo import http
from odoo.http import request


class TaxDeclarationController(http.Controller):

    @http.route('/tax_declaration', website=True, auth='public')
    def taxdeclare_form(self, **kw):
        # getting login user autometically
        userid = request.env.user.employee_id

        # getting financial year
        c_year = request.env['account.fiscal.year'].sudo().search([])

        # update and changeing amount
        # amount = request.env['employee.tax.declaration'].sudo().search([])

        autofill_data = {
            'user': userid,
            'c_year': c_year,
        }

        return request.render("tax_declare_module.create_taxdeclaration", autofill_data)

    @http.route('/create/NewTaxDeclaration', website=True, auth='public')
    def taxdeclare_submit(self, **kw):
        # getting login user autometically
        userid = request.env.user.employee_id

        # getting financial year
        c_year = request.env['account.fiscal.year'].sudo().search([])

        if kw:
            Attachment = request.env['ir.attachment']
            file_name = kw.get('attachment').filename
            file = kw.get('attachment')
            attachment_id = Attachment.create({
                'name': file_name,
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
                'res_model': userid._name,
                'res_id': userid.id
            })
            userid.update({
                'attachment': [(4, attachment_id.id)],
            })

            vals = {
                'name': userid.id,
                'c_year': c_year.id,
                'clife_amount': kw.get('coneamt') or 0.0,
                'cprovident_amount': kw.get('ctwoamt') or 0.0,
                'csubscript_amount': kw.get('cthreeamt') or 0.0,
                'ctution_amount': kw.get('cfouramt') or 0.0,
                'cnational_amount': kw.get('cfiveamt') or 0.0,
                'chouse_amount': kw.get('csixamt') or 0.0,
                'cother_amount': kw.get('csevenamt') or 0.0,
                'eightccc_amount': kw.get('cccamt') or 0.0,
                'eightccdone_amount': kw.get('ccdcamt') or 0.0,
                'eightccdoneb_amount': kw.get('ccdonebamt') or 0.0,
                'ccdtwostate_amount': kw.get('ccdfirstamt') or 0.0,
                'ccdtwocentral_amount': kw.get('ccdsecamt') or 0.0,
                'seconedepend_amount': kw.get('dstateamt') or 0.0,
                'seconeparent_amount': kw.get('dcentralamt') or 0.0,
                'sectwodepend_amount': kw.get('dstatetwoamt') or 0.0,
                'sectwoparent_amount': kw.get('dcentraltwoamt') or 0.0,
                'eightdd_amount': kw.get('ddamt') or 0.0,
                'eightddb_amount': kw.get('ddbamt') or 0.0,
                'eighte_amount': kw.get('eamt') or 0.0,
                'eightee_amount': kw.get('eeamt') or 0.0,
                'eighteea_amount': kw.get('eeaamt') or 0.0,
                'eighteeb_amount': kw.get('eebamt') or 0.0,
                'ggwithout_amount': kw.get('limitamt') or 0.0,
                'ggsubject_amount': kw.get('subjectamt') or 0.0,
                'eightgg_amount': kw.get('ggamt') or 0.0,
                'eightgga_amount': kw.get('ggaamt') or 0.0,
                'eightggc_amount': kw.get('ggcamt') or 0.0,
                'eighttta_amount': kw.get('ttaamt') or 0.0,
                'eightttb_amount': kw.get('ttbamt') or 0.0,
                'eightu_amount': kw.get('uamt') or 0.0,
            }

            create_record = request.env['employee.tax.declaration'].sudo().create(vals)

        return request.render("tax_declare_module.taxdeclare_thanks")
