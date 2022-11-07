from odoo import models, api, fields, _
import base64
import csv
import io
from tempfile import TemporaryFile
import pandas as pd
import datetime
from datetime import datetime


class ContraVoucher(models.Model):
    _name = 'contra.voucher'

    upload_contra_file = fields.Binary('File')

    def convert_to_df(self):
        csv_data = self.upload_contra_file
        file_obj = TemporaryFile('wb+')
        csv_data = base64.decodebytes(csv_data)
        file_obj.write(csv_data)
        file_obj.seek(0)
        return pd.read_csv(file_obj).fillna(False)

    def import_contra_voucher(self):
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

        action_conf = self.env['account.move']

        for rec in b:
            key_list = []
            key_list.append(rec.keys())
            date = None
            if 'Date' in rec.keys():
                date = rec['Date']
            if 'Particulars' in rec.keys():
                customer = rec['Particulars']
            if 'Voucher Type' in rec.keys():
                voucher_type = rec['Voucher Type']
            if 'Voucher No.' in rec.keys():
                voucher_no = rec['Voucher No.']
            if 'Narration' in rec.keys():
                narration = rec['Narration']
            if 'Gross Total' in rec.keys():
                gross = rec['Gross Total']
                gross_total = float(gross[:-2])
                gross_total_sufix = gross[-2:]
            print(rec, "recccc")
            keys_list = [key for key, val in rec.items() if val]
            c.append(keys_list)

            new_date = date.replace(" ", "/")
            date = datetime.strptime(new_date, '%d/%b/%y')

            for i in c:
                if 'Date' in i:
                    i.remove('Date')
                if 'Particulars' in i:
                    i.remove('Particulars')
                if 'Address' in i:
                    i.remove('Address')
                if 'GSTIN/UIN' in i:
                    i.remove('GSTIN/UIN')
                if 'PAN No.' in i:
                    i.remove('PAN No.')
                if 'Voucher Ref. Date' in i:
                    i.remove('Voucher Ref. Date')
                if 'Voucher Type' in i:
                    i.remove('Voucher Type')
                if 'Voucher No.' in i:
                    i.remove('Voucher No.')
                if 'Narration' in i:
                    i.remove('Narration')
                if 'Gross Total' in i:
                    i.remove('Gross Total')
                print(i, 'clean data')
                journal_entry_id = False
                c = []
                if '\n' in customer:
                    bank = customer.replace('\n', '')
                else:
                    bank = customer

                search_journal = self.env['account.journal'].search([('name', '=', 'Payment Register')])
                search_journal_entry = self.env['account.move'].search(
                    [('ref', '=', voucher_no), ('journal_id', '=', search_journal.id)])
                search_currency = self.env['res.currency'].search([('name', '=', 'INR')])
                account = self.env['account.account'].search([('name', '=', customer.strip())])

                journal_items = []
                journal_value = {
                    'ref': voucher_no,
                    'date': date,
                    'journal_id': search_journal.id,
                    'currency_id': search_currency.id
                }
                if not search_journal_entry:
                    journal_entry_id = search_journal_entry.sudo().create(journal_value)

                    if gross_total_sufix == 'Cr':
                        journal_value_id = (0, 0, {

                            'account_id': account.id,
                            'currency_id': search_currency.id,
                            'credit': gross_total
                        })
                        journal_items.append(journal_value_id)
                    else:
                        journal_value_id = (0, 0, {

                            'account_id': account.id,
                            'currency_id': search_currency.id,
                            'debit': gross_total
                        })
                        journal_items.append(journal_value_id)
                    for key in i:
                        if len(key) > 0:
                            # bank = key
                            if '\n' in bank:
                                bank = key.replace('\n', '')
                            else:
                                bank = key
                            print(bank, 'bank')
                            total_value = rec[str(key)]
                            total_cost = float(total_value[:-2])
                            total_cost_sufix = total_value[-2:]

                            search_bank = self.env['account.account'].search([('name', '=', bank.strip())])

                            if total_cost_sufix == 'Cr':
                                journal_value_id = (0, 0, {
                                    'account_id': search_bank.id,
                                    'currency_id': search_currency.id,
                                    'credit': total_cost
                                })
                                journal_items.append(journal_value_id)
                            else:
                                journal_value_id = (0, 0, {
                                    'account_id': search_bank.id,
                                    'currency_id': search_currency.id,
                                    'debit': total_cost
                                })
                                journal_items.append(journal_value_id)

                        else:
                            if total_cost_sufix == 'Cr':
                                journal_value_id = (0, 0, {
                                    'account_id': search_bank.id,
                                    'currency_id': search_currency.id,
                                    'credit': total_cost
                                })
                                journal_items.append(journal_value_id)
                            else:
                                journal_value_id = (0, 0, {
                                    'account_id': search_bank.id,
                                    'currency_id': search_currency.id,
                                    'debit': total_cost
                                })
                                journal_items.append(journal_value_id)

                    journal_entry_id.write({'line_ids': journal_items})
                    print(journal_items, 'journal_items')
                    journal_entry_id.action_post()
