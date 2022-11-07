from odoo import models, api, fields, _
import base64
import csv
import io
from tempfile import TemporaryFile
import pandas as pd
import datetime
from datetime import datetime


class VendorBills(models.Model):
    _name = 'vendor.bills'

    upload_file = fields.Binary('File')

    def convert_to_df(self):
        csv_data = self.upload_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        return pd.read_csv(file_obj).fillna(False)

    def import_vendor_bills(self):
        global vendor_bill_id, tax, address, gstin
        gst = False
        igst = False
        supplier_invoice_no = None
        tax_gst = False
        df = self.convert_to_df()
        data = df.to_dict('index')
        b = []  # b is list of dictionary with data of each row
        for rec in data.values():
            data = {}
            for i, j in rec.items():
                if j is not False:
                    data[i] = j
            b.append(data)
        c = []  # c is list of column names with data  of each row
        key_list = []

        action_conf = self.env['account.move']
        for rec in b:
            tax = False
            address = None
            gstin = None
            tax_value = False
            tax_gst = False
            vendor_bill_id = False
            sgst = False
            cgst = False
            customer = False
            supplier = False
            voucher_no = False
            voucher_type = False
            date = False
            supplier_invoice_date = False
            pan_no = False
            narration = False

            key_list.append(rec.keys())
            if 'Date' in rec.keys():
                date = rec['Date']
            if 'Particulars' in rec.keys():
                customer = rec['Particulars']
            if 'Supplier' in rec.keys():
                supplier = rec['Supplier']
            if 'Address' in rec.keys():
                address = rec['Address']
            if 'Voucher Type' in rec.keys():
                voucher_type = rec['Voucher Type']
            if 'Voucher No.' in rec.keys():
                voucher_no = rec['Voucher No.']
            elif 'Supplier Invoice No.' in rec.keys():
                supplier_invoice_no = rec['Supplier Invoice No.']
            else:
                supplier_invoice_no = 0
            if 'Supplier Invoice Date' in rec.keys():
                supplier_invoice_date = rec['Supplier Invoice Date']
            if 'GSTIN/UIN' in rec.keys():
                gstin = rec['GSTIN/UIN']
            if 'Sales Tax No.' in rec.keys():
                sales_tax_no = rec['Sales Tax No.']
            if 'Service Tax No.' in rec.keys():
                service_tax_no = rec['Service Tax No.']
            if 'PAN No.' in rec.keys():
                pan_no = rec['PAN No.']
            if 'Narration' in rec.keys():
                narration = rec['Narration']
            if 'Quantity' in rec.keys():
                quantity = rec['Quantity']
            if 'Alt. Units' in rec.keys():
                alt_units = rec['Alt. Units']
            if 'Rate' in rec.keys():
                rate = rec['Rate']
            if 'Value' in rec.keys():
                value = rec['Value']
            if 'Addl. Cost' in rec.keys():
                add_cost = rec['Addl. Cost']
            if 'Gross Total' in rec.keys():
                gross_total = rec['Gross Total']
            if 'Rent of Guest House' in rec.keys():
                rent_guest_house = rec['Rent of Guest House']
            if 'TDS Payable - 194I A.Y. 2023-24' in rec.keys():
                tds_payable = rec['TDS Payable - 194I A.Y. 2023-24']
            if 'Warehousing Charges' in rec.keys():
                warehouse_charges = rec['Warehousing Charges']
            if 'CGST' in rec.keys():
                cgst = rec['CGST']
            if 'SGST' in rec.keys():
                sgst = rec['SGST']
            if 'Accomodation Expenses' in rec.keys():
                accomodation = rec['Accomodation Expenses']
            if 'GST Rate' in rec.keys():
                tax = rec['GST Rate']
            if 'IGST' in rec.keys():
                igst = rec['IGST']
            print(rec, "recccc")
            keys_list = [key for key, val in rec.items() if val]
            c.append(keys_list)

            for i in c:  # i is particular row
                if 'Date' in i:
                    i.remove('Date')
                if 'Particulars' in i:
                    i.remove('Particulars')
                if 'Supplier' in i:
                    i.remove('Supplier')
                if 'Address' in i:
                    i.remove('Address')
                if 'Voucher Type' in i:
                    i.remove('Voucher Type')
                if 'Voucher No.' in i:
                    i.remove('Voucher No.')
                if 'Supplier Invoice No.' in i:
                    i.remove('Supplier Invoice No.')
                if 'Supplier Invoice Date' in i:
                    i.remove('Supplier Invoice Date')
                if 'GSTIN/UIN' in i:
                    i.remove('GSTIN/UIN')
                if 'PAN No.' in i:
                    i.remove('PAN No.')
                if 'Narration' in i:
                    i.remove('Narration')
                if 'Gross Total' in i:
                    i.remove('Gross Total')
                if 'GST Rate' in i:
                    i.remove('GST Rate')
                if 'SGST' in i:
                    i.remove('SGST')
                if 'CGST' in i:
                    i.remove('CGST')
                if 'IGST' in i:
                    i.remove('IGST')
                if 'Voucher Ref. No.' in i:
                    i.remove('Voucher Ref. No.')
                if 'Voucher Ref. Date' in i:
                    i.remove('Voucher Ref. Date')
                print(i, 'clean data')
                tds_values = ['TDS Payable- 194C A.Y. 2023-24', 'TDS Payable - 194J A.Y. 2023-24',
                              'TDS Payable - 194B A.Y. 2023-24', 'TDS Payable - 194I A.Y. 2023-24']
                taxes = []
                data_without_tds = []
                data_with_tds = []
                for m in i:
                    if m in tds_values:
                        data_with_tds.append(m)
                    else:
                        data_without_tds.append(m)

            #    now row data is cleaned
            search_customer = self.env['res.partner'].search([('name', '=', customer)])
            search_supplier = self.env['res.partner'].search([('name', '=', supplier)])
            search_vendor_bill = self.env['account.move'].search(
                [('payment_reference', '=', voucher_no), ('voucher_type', '=', voucher_type)])
            if not search_vendor_bill:
                if date:
                    new_date = date.replace(" ", "/")
                    date = datetime.strptime(new_date, '%d/%b/%y')
                if supplier_invoice_date:
                    new_invoice_date = supplier_invoice_date.replace(" ", "/")
                    supplier_invoice_date = datetime.strptime(new_invoice_date, '%d/%b/%y')
                search_product = self.env['product.product'].search([('name', '=', 'Services')])

                # compute tax weather it is gst or igst
                if tax:
                    if sgst:
                        tax_value = 'GST' + ' ' + tax
                    if igst:
                        tax_value = 'IGST' + ' ' + tax

                if tax_value:
                    gst_type = self.env['account.tax'].search(
                        [('name', '=', tax_value), ('type_tax_use', '=', 'purchase')])
                    gst = gst_type.id
                    taxes.append(gst)
                vendor_lst = []

                if not address:
                    address = None

                if not gstin:
                    gstin = None

                if not search_customer:  # create customer if not created if not gstin type is set to unregistered else regular
                    if gstin:
                        customer_vals = {
                            'name': customer,
                            'l10n_in_gst_treatment': 'regular',
                            'street': address,
                            'pan_no': pan_no,
                            'vat': gstin,
                        }
                        search_customer = self.env['res.partner'].create(customer_vals)
                    else:
                        customer_vals = {
                            'name': customer,
                            'l10n_in_gst_treatment': 'unregistered',
                            'street': address,
                            'pan_no': pan_no,
                            'vat': gstin,
                        }
                        search_customer = self.env['res.partner'].create(customer_vals)
                # create vendor bill if payment_reference (i.e:- reference invoice number) is new
                vendor_bills_values = {
                    'move_type': 'in_invoice',
                    # 'name': supplier_invoice_no,
                    'ref': supplier_invoice_no,
                    'voucher_type': voucher_type,
                    'payment_reference': voucher_no,
                    'partner_id': search_customer.id,
                    'invoice_date': date,  # change to date supplier_invoice_date
                    'date': date,
                    'l10n_in_gst_treatment': 'regular',
                }
                if not search_vendor_bill:
                    vendor_bill_id = search_vendor_bill.sudo().create(vendor_bills_values)
                    # FOR loop on clean data z is key
                    print(data_without_tds, 'data without tds')
                    for key in data_without_tds:
                        coa = self.env['account.account'].search([('name', '=', key)])
                        value = rec[key]
                        print(rec[key], 'key')  # get value
                        gross_total = float(value[:-3])
                        if len(data_with_tds) > 0:
                            for tds_data in data_with_tds:
                                tds = self.env['account.tax'].search([('name', '=', tds_data)])
                                taxes.append(tds.id)
                        else:
                            pass
                        print(taxes, 'taxes')
                        if key == 'Cancellation Charges' or key == 'Cancellation Charges - HO' or key == 'Discount':
                            gross_total = -(gross_total)
                        if len(taxes) > 0:
                            if key == 'Travelling Expenses' or key == 'Ineligible ITC-IGST' or key == 'Travelling Expenses-HO' or key == 'Discount':
                                vendor_bill_vals_ids = (0, 0, {
                                    'product_id': search_product.id,
                                    'name': voucher_type,
                                    'account_id': coa.id,
                                    'price_unit': gross_total,
                                })
                                vendor_lst.append(vendor_bill_vals_ids)
                            else:
                                print(taxes, 'taxessss')
                                vendor_bill_vals_ids = (0, 0, {
                                    'product_id': search_product.id,
                                    'name': voucher_type,
                                    'account_id': coa.id,
                                    'price_unit': gross_total,
                                    'tax_ids': [(4, tax) for tax in taxes]
                                })
                                vendor_lst.append(vendor_bill_vals_ids)
                        else:
                            vendor_bill_vals_ids = (0, 0, {
                                'product_id': search_product.id,
                                'name': voucher_type,
                                'account_id': coa.id,
                                'price_unit': gross_total,
                            })
                            vendor_lst.append(vendor_bill_vals_ids)

                    vendor_bill_id.write({'invoice_line_ids': vendor_lst, 'narration': narration})
                    vendor_bill_id.action_post()
