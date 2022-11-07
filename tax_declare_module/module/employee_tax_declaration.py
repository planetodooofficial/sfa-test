from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class EmployeeTaxDeclaration(models.Model):
    _name = "employee.tax.declaration"

    state = fields.Selection([('draft', "Draft"),
                              ('submitted', "Submitted"),
                              ('approved', "Approved")],
                             string='Status', readonly=True, default='draft')

    # one 2 many with hr.employee inherited class
    name = fields.Many2one('hr.employee', 'Employee Name', default=lambda self: self.env.user.employee_id)

    # Financial year getting from account.fiscal.year
    c_year = fields.Many2one('account.fiscal.year', 'Year')

    # 80C
    clife_amount = fields.Float('Amount')
    clife_document = fields.Binary('Upload File')
    cfilename = fields.Char(string='File Name')

    cprovident_amount = fields.Float('Amount')
    cprovident_document = fields.Binary('Upload File')
    cpfilename = fields.Char(string='File Name')

    csubscript_amount = fields.Float('Amount')
    csubscript_document = fields.Binary('Upload File')
    csfilename = fields.Char(string='File Name')

    ctution_amount = fields.Float('Amount')
    ctution_document = fields.Binary('Upload File')
    ctfilename = fields.Char(string='File Name')

    cnational_amount = fields.Float('Amount')
    cnational_document = fields.Binary('Upload File')
    cnfilename = fields.Char(string='File Name')

    chouse_amount = fields.Float('Amount')
    chouse_document = fields.Binary('Upload File')
    chfilename = fields.Char(string='File Name')

    cother_amount = fields.Float('Amount')
    cother_document = fields.Binary('Upload File')
    cofilename = fields.Char(string='File Name')

    # 80CCC
    eightccc_amount = fields.Float('80CCC Amount')
    eightccc_document = fields.Binary('80CCC Document')
    cccfilename = fields.Char(string='File Name')

    # 80CCD(1)
    eightccdone_amount = fields.Float('80CCD(1) Amount')
    eightccdone_document = fields.Binary('80CCD(1) Document')
    ccdfilename = fields.Char(string='File Name')

    # 80CCD(1B)
    eightccdoneb_amount = fields.Float('80CCD(1B) Amount')
    eightccdoneb_document = fields.Binary('80CCD(1B) Document')
    ccdbfilename = fields.Char(string='File Name')

    # 80CCD(2)
    ccdtwostate_amount = fields.Float('Amount')
    ccdtwostate_document = fields.Binary('Upload File')
    ccdtfilename = fields.Char(string='File Name')

    ccdtwocentral_amount = fields.Float('Amount')
    ccdtwocentral_document = fields.Binary('Upload File')
    ccdtcfilename = fields.Char(string='File Name')

    # 80D section1
    seconedepend_amount = fields.Float('Amount')
    seconedepend_document = fields.Binary('Upload File')
    sdfilename = fields.Char(string='File Name')

    seconeparent_amount = fields.Float('Amount')
    seconeparent_document = fields.Binary('Upload File')
    spfilename = fields.Char(string='File Name')

    # 80D section2
    sectwodepend_amount = fields.Float('Amount')
    sectwodepend_document = fields.Binary('Upload File')
    scfilename = fields.Char(string='File Name')

    sectwoparent_amount = fields.Float('Amount')
    sectwoparent_document = fields.Binary('Upload File')
    scpfilename = fields.Char(string='File Name')

    # 80DD
    eightdd_amount = fields.Float('80DD Amount')
    eightdd_document = fields.Binary('80DD Document')
    ddfilename = fields.Char(string='File Name')

    # 80DDB
    eightddb_amount = fields.Float('80DDB Amount')
    eightddb_document = fields.Binary('80DDB Document')
    ddbfilename = fields.Char(string='File Name')

    # 80E
    eighte_amount = fields.Float('80E Amount')
    eighte_document = fields.Binary('80E Document')
    efilename = fields.Char(string='File Name')

    # 80EE
    eightee_amount = fields.Float('80EE Amount')
    eightee_document = fields.Binary('80EE Document')
    eefilename = fields.Char(string='File Name')

    # 80EEA
    eighteea_amount = fields.Float('80EEA Amount')
    eighteea_document = fields.Binary('80EEA Document')
    eeafilename = fields.Char(string='File Name')

    # 80EEB
    eighteeb_amount = fields.Float('80EEB Amount')
    eighteeb_document = fields.Binary('80EEB Document')
    eebfilename = fields.Char(string='File Name')

    # 80G
    ggwithout_amount = fields.Float('Amount')
    ggwithout_document = fields.Binary('Upload Document')
    ggwfilename = fields.Char(string='File Name')

    ggsubject_amount = fields.Float('Amount')
    ggsubject_document = fields.Binary('Upload Document')
    ggsfilename = fields.Char(string='File Name')

    # 80GG
    eightgg_amount = fields.Float('80GG Amount')
    eightgg_document = fields.Binary('80GG Document')
    ggfilename = fields.Char(string='File Name')

    # 80GGA
    eightgga_amount = fields.Float('80GGA Amount')
    eightgga_document = fields.Binary('80GGA Document')
    ggafilename = fields.Char(string='File Name')

    # 80GGC
    eightggc_amount = fields.Float('80GGC Amount')
    eightggc_document = fields.Binary('80GGC Document')
    ggcfilename = fields.Char(string='File Name')

    # 80TTA
    eighttta_amount = fields.Float('80TTA Amount')
    eighttta_document = fields.Binary('80TTA Document')
    ttafilename = fields.Char(string='File Name')

    # 80TTB
    eightttb_amount = fields.Float('80TTB Amount')
    eightttb_document = fields.Binary('80TTB Document')
    ttbfilename = fields.Char(string='File Name')

    # 80U
    eightu_amount = fields.Float('80U Amount')
    eightu_document = fields.Binary('80U Document')
    ufilename = fields.Char(string='File Name')

    # # store attachments in our model
    attachment = fields.Many2many('ir.attachment', 'attach_rel', 'doc_id', 'attach_id', string="Attachment",
                                  help='You can upload your document', copy=False)

    def tax_declaration_approve(self):
        self.state = 'approved'

    def tax_declaration_submit(self):
        self.state = 'submitted'

    def tax_declaration_reset(self):
        self.state = 'draft'

    # for avoid duplicate entry with same name with same year
    @api.model
    def create(self, vals):
        a = self.search([])
        for i in a:
            if i.name.id == vals['name'] and i.c_year.id == vals['c_year']:
                raise ValidationError(_('This Record is already Exist, please select another User or Financial Year'))
        res = super(EmployeeTaxDeclaration, self).create(vals)
        return res


class Attachment(models.Model):
    _inherit = 'ir.attachment'
    attach_rel = fields.Many2many('employee.tax.declaration', 'attachment', 'attachment_id', 'document_id',
                                  string="Attachment")
