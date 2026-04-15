# 📄 Payloads Reference

This directory contains the editable payloads for POST/PUT API operations.

## 🎯 How to Use

1. **Edit the JSON file** corresponding to the desired operation
2. **Run the CLI** (`python -m src.cli`)
3. **Choose the operation** in the menu
4. **See the result** in the terminal

## 📋 Available Files

### transaction-create.json
Create a new payment transaction.

**Main fields:**
- `amount`: Value in cents (10000 = R$ 100.00)
- `payment_method`: "credit_card", "boleto", "pix"
- `card_hash`: Card hash (generated on the frontend)
- `customer`: Customer data
- `items`: List of products/services

### customer-create.json
Create a new customer.

**Main fields:**
- `name`: Full name
- `email`: Valid email
- `documents`: Array with CPF/CNPJ
- `phone_numbers`: Array of phone numbers

### payment-link-create.json
Create a hosted payment link.

**Main fields:**
- `amount`: Value in cents
- `payment_methods`: Array of accepted methods (e.g.: ["pix", "credit_card", "boleto"])
- `max_installments`: Maximum number of installments
- `success_url`: Return URL after payment
- `description`: Payment description

### payment-link-update.json
Update an existing payment link.

### recipient-create.json
Create a recipient for payment split.

**Main fields:**
- `transfer_interval`: "daily", "weekly", "monthly"
- `transfer_enabled`: true/false
- `bank_account`: Bank account data

### recipient-update.json
Update a recipient's settings.

### bank-account-create.json
Create a bank account.

**Main fields:**
- `bank_code`: Bank code (e.g.: "001", "237", "341")
- `agencia`: Branch number
- `conta`: Account number
- `conta_dv`: Check digit
- `type`: "conta_corrente" or "conta_poupanca"

### transfer-create.json
Create a transfer.

**Option 1 - With recipient_id:**
```json
{
  "amount": 50000,
  "recipient_id": "re_abc123"
}
```

**Option 2 - With bank_account:**
```json
{
  "amount": 50000,
  "bank_account": { ... }
}
```

### company-update.json
Update company data.

### delivery-update.json
Update the delivery status of a transaction.

**Valid statuses:**
- "processing"
- "shipped"
- "delivered"
- "returned"

## 💡 Tips

### Testing Multiple Scenarios

Create variations to test:
- Different values
- Different payment methods
- Optional fields filled/empty
- Invalid data (to see error handling)

### Values in Cents

**Important:** All monetary values are in cents!

```
R$ 1.00    = 100 cents
R$ 10.00   = 1000 cents
R$ 100.00  = 10000 cents
R$ 1,000.00 = 100000 cents
```

### Dynamic IDs

For operations that require IDs (GET, refund, update), the CLI will ask for the ID at execution time. You don't need to edit payloads for that.

### Unique Emails

To create multiple customers or payment links, vary the email:
- `test1@example.com`
- `test2@example.com`
- or use timestamp: `test${Date.now()}@example.com` (do it manually)

## 🔄 Recommended Workflow

1. **First:** List existing resources (List)
2. **Copy IDs** you want to manipulate
3. **Edit payloads** as needed
4. **Run operations** CREATE/UPDATE
5. **Verify results** with GET

## ⚠️ Important Notes

- **card_hash:** To create transactions, you need a valid card_hash generated on the frontend
- **Environment:** Make sure you are using the correct credentials (sandbox/production)
- **Balance:** Transfers require available balance in the account

---

💡 **Tip:** Use Ctrl+C to exit the CLI at any time