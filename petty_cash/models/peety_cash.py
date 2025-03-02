from odoo import fields, models, api,_,Command
from num2words import num2words
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    accounts = fields.Many2one(
        'account.account',
        string='Accounts',)

    amount_in_words_ar =fields.Char(string='Amount in Words', compute='_compute_amount_in_words')
    # amount_in_words_en =fields.Char(string='Amount in Words', compute='_compute_amount_in_words')
    check_number = fields.Char(string='Check Number',readonly=False,)
    due_date = fields.Date(string='Due Date')
    analytic_line_ids = fields.One2many(
        comodel_name='account.analytic.line', inverse_name='move_line_id',
        string='Analytic lines',)
    analytic_distribution = fields.Json(store=True, string="Analytic Distribution")
    analytic_precision = fields.Integer(
        store=False,
        default=lambda self: self.env['decimal.precision'].precision_get("Percentage Analytic"),)
    payment_type_new = fields.Selection(
        string='Payment_type',
        selection=[('accounts', 'Accounts'),
                   ('receivable', 'Receivable'),('payable', 'Payable'), ],
        required=True, )
        


    @api.depends('amount', 'journal_id')
    def _compute_amount_in_words(self):
        for record in self:
            if record.journal_id.type in ['bank', 'cash']:
                whole_part = int(record.amount)
                fractional_part = round(record.amount - whole_part, 2)
                whole_in_words = num2words(whole_part, to='cardinal', lang='ar')
                # whole_in_words_en = num2words(whole_part, to='cardinal', lang='en')
                if fractional_part > 0:
                    fractional_in_words = num2words(int(fractional_part * 100), to='cardinal', lang='ar')
                    # fractional_in_words_en = num2words(int(fractional_part * 100), to='cardinal', lang='en')
                    record.amount_in_words_ar = f"{whole_in_words}  جنيهاً و {fractional_in_words} قرشًا"
                    # record.amount_in_words_en = f"{whole_in_words_en} Pounds and {fractional_in_words_en} Piasters"
                else:
                    record.amount_in_words_ar =f"{whole_in_words} جنيها  ً"
                    # record.amount_in_words_en =f"{whole_in_words_en} Pounds"
            else:
                record.amount_in_words_ar = ''
                # record.amount_in_words_en = ''

    def _seek_for_lines(self):
        ''' Helper used to dispatch the journal items between:
        - The lines using the temporary liquidity account.
        - The lines using the counterpart account.
        - The lines being the write-off lines.
        :return: (liquidity_lines, counterpart_lines, write_off_lines)
        '''
        self.ensure_one()

        liquidity_lines = self.env['account.move.line']
        counterpart_lines = self.env['account.move.line']
        writeoff_lines = self.env['account.move.line']

        for line in self.move_id.line_ids:
            if line.account_id in self._get_valid_liquidity_accounts() :
                liquidity_lines += line
            elif (line.account_id.account_type in ('asset_receivable', 'liability_payable') or line.partner_id == line.company_id.partner_id) and len(counterpart_lines)==0 :
                print("before>>>>>>>>>>>>",counterpart_lines)
                counterpart_lines += line
                print("after", counterpart_lines)
            else:
                writeoff_lines += line
        return liquidity_lines, counterpart_lines, writeoff_lines

    # @api.depends('journal_id', 'partner_id', 'partner_type', 'is_internal_transfer', 'destination_journal_id')
    # def _compute_destination_account_id(self):
    #     self.destination_account_id = False
    #     for pay in self:
    #         if pay.is_internal_transfer:
    #             pay.destination_account_id = pay.destination_journal_id.company_id.transfer_account_id
    #         elif pay.partner_type == 'customer':
    #             if pay.partner_id:
    #                 pay.destination_account_id = pay.partner_id.with_company(pay.company_id).property_account_receivable_id
    #             else:
    #                 pay.destination_account_id = self.env['account.account'].search([
    #                     ('company_id', '=', pay.company_id.id),
    #                     ('account_type', '=', 'asset_receivable'),
    #                     ('deprecated', '=', False),
    #                 ], limit=1)
    #
    #         elif pay.partner_type == 'supplier':
    #             # Send money to pay a bill or receive money to refund it.
    #             if pay.partner_id:
    #                 pay.destination_account_id = pay.accounts.id or pay.partner_id.with_company(
    #                     pay.company_id).property_account_payable_id
    #             else:
    #                 pay.destination_account_id = self.env['account.account'].search([
    #                     ('company_id', '=', pay.company_id.id),
    #                     ('account_type', '=', 'liability_payable'),
    #                     ('deprecated', '=', False),
    #                 ], limit=1)


    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        ''' Prepare the dictionary to create the default account.move.lines for the current payment.
        :param write_off_line_vals: Optional list of dictionaries to create a write-off account.move.line easily containing:
            * amount:       The amount to be added to the counterpart amount.
            * name:         The label to set on the line.
            * account_id:   The account on which create the write-off.
        :return: A list of python dictionary to be passed to the account.move.line's 'create' method.
        '''
        self.ensure_one()
        write_off_line_vals = write_off_line_vals or {}

        if not self.outstanding_account_id:
            raise UserError(_(
                "You can't create a new payment without an outstanding payments/receipts account set either on the company or the %s payment method in the %s journal.",
                self.payment_method_line_id.name, self.journal_id.display_name))

        # Compute amounts.
        write_off_line_vals_list = write_off_line_vals or []
        write_off_amount_currency = sum(x['amount_currency'] for x in write_off_line_vals_list)
        write_off_balance = sum(x['balance'] for x in write_off_line_vals_list)
        if self.payment_type == 'inbound': #receive
            liquidity_amount_currency = self.amount
        elif self.payment_type == 'outbound':   #send
            liquidity_amount_currency = -self.amount
        else:
            liquidity_amount_currency = 0.0

        liquidity_balance = self.currency_id._convert(
            liquidity_amount_currency,
            self.company_id.currency_id,
            self.company_id,
            self.date,
        )
        counterpart_amount_currency = -liquidity_amount_currency - write_off_amount_currency
        counterpart_balance = -liquidity_balance - write_off_balance
        currency_id = self.currency_id.id

        # Compute a default label to set on the journal items.
        liquidity_line_name = ''.join(x[1] for x in self._get_liquidity_aml_display_name_list())
        counterpart_line_name = ''.join(x[1] for x in self._get_counterpart_aml_display_name_list())
        line_vals_list = [
            # Liquidity line.
            {
                'name': liquidity_line_name,
                'date_maturity': self.date,
                'amount_currency': liquidity_amount_currency,
                'currency_id': currency_id,
                'debit': liquidity_balance if liquidity_balance > 0.0 else 0.0,
                'credit': -liquidity_balance if liquidity_balance < 0.0 else 0.0,
                'analytic_distribution': self.analytic_distribution,
                'partner_id': self.partner_id.id,
                'account_id': self.outstanding_account_id.id,
            },
            # Receivable / Payable.
            {
                'name': counterpart_line_name,
                'date_maturity': self.date,
                'amount_currency': counterpart_amount_currency,
                'currency_id': currency_id,
                'debit': counterpart_balance if counterpart_balance > 0.0 else 0.0,
                'credit': -counterpart_balance if counterpart_balance < 0.0 else 0.0,
                'analytic_distribution':self.analytic_distribution,
                'partner_id': self.partner_id.id,
                'account_id':self.destination_account_id.id,
            },
        ]
        print("line_vals_list",)

        return line_vals_list + write_off_line_vals_list

    def _synchronize_from_moves(self, changed_fields):
        ''' Update the account.payment regarding its related account.move.
        Also, check both models are still consistent.
        :param changed_fields: A set containing all modified fields on account.move.
        '''
        if self._context.get('skip_account_move_synchronization'):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):

            # After the migration to 14.0, the journal entry could be shared between the account.payment and the
            # account.bank.statement.line. In that case, the synchronization will only be made with the statement line.
            if pay.move_id.statement_line_id:
                continue

            move = pay.move_id
            move_vals_to_write = {}
            payment_vals_to_write = {}
            if 'journal_id' in changed_fields:
                if pay.journal_id.type not in ('bank', 'cash'):
                    raise UserError(_("A payment must always belongs to a bank or cash journal."))

            if 'line_ids' in changed_fields:
                all_lines = move.line_ids
                liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()
                if len(liquidity_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one outstanding payments/receipts account.",
                        move.display_name,
                    ))

                if len(counterpart_lines) != 1:
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "include one and only one receivable/payable account (with an exception of "
                        "internal transfers).",
                        move.display_name,
                    ))

                if any(line.currency_id != all_lines[0].currency_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same currency.",
                        move.display_name,
                    ))

                if any(line.partner_id != all_lines[0].partner_id for line in all_lines):
                    raise UserError(_(
                        "Journal Entry %s is not valid. In order to proceed, the journal items must "
                        "share the same partner.",
                        move.display_name,
                    ))

                if counterpart_lines.account_id.account_type == 'asset_receivable':
                    partner_type = 'customer'
                else:
                    partner_type = 'supplier'

                liquidity_amount = liquidity_lines.amount_currency

                move_vals_to_write.update({
                    'currency_id': liquidity_lines.currency_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                payment_vals_to_write.update({
                    'amount': abs(liquidity_amount),
                    'partner_type': partner_type,
                    'currency_id': liquidity_lines.currency_id.id,
                    'destination_account_id': counterpart_lines.account_id.id,
                    'partner_id': liquidity_lines.partner_id.id,
                })
                if liquidity_amount > 0.0:
                    payment_vals_to_write.update({'payment_type': 'inbound'})
                elif liquidity_amount < 0.0:
                    payment_vals_to_write.update({'payment_type': 'outbound'})

            move.write(move._cleanup_write_orm_values(move, move_vals_to_write))
            pay.write(move._cleanup_write_orm_values(pay, payment_vals_to_write))

    def _synchronize_to_moves(self, changed_fields):
        ''' Update the account.move regarding the modified account.payment.
        :param changed_fields: A list containing all modified fields on account.payment.
        '''
        print("_synchronize_to_moves")
        if self._context.get('skip_account_move_synchronization'):
            return

        if not any(field_name in changed_fields for field_name in self._get_trigger_fields_to_synchronize()):
            return

        for pay in self.with_context(skip_account_move_synchronization=True):
            liquidity_lines, counterpart_lines, writeoff_lines = pay._seek_for_lines()

            # Make sure to preserve the write-off amount.
            # This allows to create a new payment with custom 'line_ids'.

            write_off_line_vals = []
            if liquidity_lines and counterpart_lines and writeoff_lines:
                write_off_line_vals.append({
                    'name': writeoff_lines[0].name,
                    'account_id': writeoff_lines[0].account_id.id,
                    'partner_id': writeoff_lines[0].partner_id.id,
                    'currency_id': writeoff_lines[0].currency_id.id,
                    'amount_currency': sum(writeoff_lines.mapped('amount_currency')),
                    'balance': sum(writeoff_lines.mapped('balance')),
                })

            line_vals_list = pay._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)

            line_ids_commands = [
                Command.update(liquidity_lines.id, line_vals_list[0]) if liquidity_lines else Command.create(line_vals_list[0]),
                Command.update(counterpart_lines.id, line_vals_list[1]) if counterpart_lines else Command.create(line_vals_list[1])
            ]

            for line in writeoff_lines:
                line_ids_commands.append((2, line.id))

            for extra_line_vals in line_vals_list[2:]:
                line_ids_commands.append((0, 0, extra_line_vals))

            # Update the existing journal items.
            # If dealing with multiple write-off lines, they are dropped and a new one is generated.

            pay.move_id\
                .with_context(skip_invoice_sync=True)\
                .write({
                    'partner_id': pay.partner_id.id,
                    'currency_id': pay.currency_id.id,
                    'partner_bank_id': pay.partner_bank_id.id,
                    'line_ids': line_ids_commands,
                })
