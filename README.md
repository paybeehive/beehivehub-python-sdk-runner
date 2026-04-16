# Beehive Hub Python SDK Runner

🚀 Interactive CLI tool to consume and validate the [beehivehub-python-sdk](https://pypi.org/project/beehivehub-python-sdk/).

## 📋 About the Project

This is an internal development project for consuming and validating all Beehive Hub SDK features in a practical, interactive way.

**This is not an automated test suite** — it's a tool for developers to run API operations manually and in a controlled way through an interactive terminal menu.

## 🚀 Quick Setup

```bash
# 0. Clone (if getting from GitHub)
git clone https://github.com/paybeehive/beehivehub-python-sdk-runner.git
cd beehivehub-python-sdk-runner

# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# 2. Install dependencies
pip install -e .

# 3. Configure .env
cp .env.example .env
BEEHIVE_SECRET_KEY=your_secret_key_here
BEEHIVE_ENVIRONMENT=sandbox  # or 'production'
# OUTPUT_DIR=./custom-output  # (optional) customize output directory

# 4. Run
python -m src.cli
```

### 🌐 Environments

The SDK supports two environments:

- **`production`** (default) — Production API
- **`sandbox`** — Sandbox/testing API

Configure in `.env`:

```env
# Production (default)
BEEHIVE_SECRET_KEY=sk_live_abc...
# BEEHIVE_ENVIRONMENT=production

# Sandbox
BEEHIVE_SECRET_KEY=sk_test_xyz...
BEEHIVE_ENVIRONMENT=sandbox
```

The current environment is shown at the top of the CLI.

## 💻 How to Use

### Run the CLI

```bash
python -m src.cli
```

You will see an interactive menu:

```
🐝 Beehive Hub SDK Runner

? Choose a resource:
  💳 Transactions
  👥 Customers
  🔗 Payment Links
  🎯 Recipients
  🏦 Bank Accounts
  💸 Transfers
  🏢 Company
  📊 Balance
  ❌ Exit
```

### 📁 Automatic Response Saving

**IMPORTANT**: All API responses are **automatically saved** to the `output/` folder in the format:

```
output/{timestamp}_{resource}_{operation}.json
```

**In the terminal you will see only a summary**, for example:

```
✅ Transaction created

📊 ID: txn_abc123xyz
📁 Full result saved to: output/2026-01-15T10-30-45_transactions_create.json
```

The complete JSON is in the file, not in the terminal! 🎯

### ⚙️ Configure Output Directory (Optional)

By default, files are saved to `./output`. To customize, add to `.env`:

```env
OUTPUT_DIR=/custom/path/output
```

### Typical Workflow

1. **Choose the resource** (e.g., Transactions)
2. **Choose the operation** (e.g., List, Get, Create)
3. **For GET:** Enter the ID when prompted
4. **For CREATE/UPDATE:** The payload from the JSON file will be used
5. **View the result** formatted in the terminal
6. **Return to the menu** for a new operation

### Edit Payloads

Payloads are located in `payloads/*.json`:

```
payloads/
├── transaction-create.json            # Create transaction
├── customer-create.json               # Create customer
├── payment-link-create.json           # Create payment link
├── payment-link-update.json           # Update payment link
├── recipient-create.json              # Create recipient
├── recipient-update.json              # Update recipient
├── bank-account-create.json           # Create bank account
├── transfer-create.json               # Transfer with recipient_id
├── transfer-create-with-account.json  # Transfer with bank account
├── company-update.json                # Update company
└── delivery-update.json               # Update delivery
```

**To test different scenarios:**
1. Edit the JSON file
2. Run the operation in the menu
3. Adjust as needed
4. Run again

## 📖 Available Resources

### 💳 Transactions
- **List Transactions** — Lists with filters (limit, offset, createdFrom, etc.)
- **Get Transaction** — Fetch by ID
- **Create Transaction** — Uses `transaction-create.json`
- **Refund Transaction** — Full or partial refund
- **Update Delivery** — Uses `delivery-update.json`

### 👥 Customers
- **List Customers** — Search by email (required; does not support pagination)
- **Get Customer** — Fetch by ID
- **Create Customer** — Uses `customer-create.json`

### 🔗 Payment Links
- **List Payment Links** — Lists all
- **Get Payment Link** — Fetch by ID
- **Create Payment Link** — Uses `payment-link-create.json`
- **Update Payment Link** — Uses `payment-link-update.json`
- **Delete Payment Link** — Removes by ID

### 🎯 Recipients
- **List Recipients** — Lists all
- **Get Recipient** — Fetch by ID
- **Create Recipient** — Uses `recipient-create.json`
- **Update Recipient** — Uses `recipient-update.json`

### 🏦 Bank Accounts
- **List Bank Accounts** — Lists by Recipient ID
- **Create Bank Account** — Uses `bank-account-create.json`

> Bank Accounts are linked to a Recipient. Provide the recipient ID to list or create.

### 💸 Transfers
- **Create Transfer** — Uses `transfer-create.json`
- **Get Transfer** — Fetch by ID

### 🏢 Company
- **Get Company Info** — Company data
- **Update Company** — Uses `company-update.json`

### 📊 Balance
- **Get Balance** — Available, pending, and transferred balance

## 📁 Project Structure

```
beehivehub-python-sdk-runner/
├── src/
│   ├── cli.py              # Main CLI entry point
│   ├── sdk.py              # SDK initialization
│   ├── check_env.py        # Environment variable validation
│   ├── utils.py            # Utility functions
│   └── resources/          # Handlers per resource
│       ├── transactions.py
│       ├── customers.py
│       ├── payment_links.py
│       ├── recipients.py
│       ├── bank_accounts.py
│       ├── transfers.py
│       ├── company.py
│       └── balance.py
├── payloads/               # Editable payloads
│   ├── *.json              # Main payloads
│   └── README.md           # Payload documentation
├── tests/                  # Test suite
├── output/                 # Auto-saved API responses (gitignored)
├── .env                    # Credentials (do not version!)
├── .env.example            # Template
├── pyproject.toml
└── README.md
```

## 🧪 Tests

The project includes a test suite to validate SDK integration:

```bash
pip install -e .
pip install ruff pytest pytest-cov
pytest
```

## 🛠️ Tech Stack

- **Python 3.10+** — Language
- **questionary** — Interactive terminal menu
- **python-dotenv** — Credential management
- **beehivehub-python-sdk** — Official SDK via PyPI

## 🔧 Update the SDK

The runner uses the SDK installed from PyPI. To update to the latest version:

```bash
pip install --upgrade beehivehub-python-sdk
```

Or reinstall from scratch:

```bash
pip install -e .
```

## 💡 Usage Examples

### Scenario 1: Create and Fetch a Customer

1. Run `python -m src.cli`
2. Choose "👥 Customers"
3. Choose "Create Customer"
4. See the returned ID (e.g., `cust_abc123`)
5. Go back and choose "Get Customer by ID"
6. Enter the ID
7. View complete data

### Scenario 2: Test Different Payment Methods

**PIX Transaction:** Edit `payloads/transaction-create.json` with `payment_method: "pix"` and run "Create Transaction".

**Installment Transaction:** Edit `payloads/transaction-create.json` with `installments` and run "Create Transaction".

### Scenario 3: Create a Payment Link and Test Payment

1. Edit `payloads/payment-link-create.json`
2. Run "Create Payment Link"
3. Copy the returned `url`
4. Open in browser to test
5. Use "Get Payment Link" to check status

## ⚠️ Important Notes

### Values in Cents

All monetary values are in cents:
- R$ 10.00 = `1000`
- R$ 100.00 = `10000`
- R$ 1,000.00 = `100000`

### Card Hash

To create card transactions, you need a valid `card_hash` generated on the frontend using the Beehive Hub JavaScript library.

### Dynamic IDs

For operations that require IDs (GET, refund, update), copy the IDs returned by creation or listing operations.

### Environment

Make sure to use the correct credentials:
- **Sandbox:** For testing without real financial movement
- **Production:** For real operations

## 🎯 Use Cases

### Validate Transaction Creation

1. Edit `payloads/transaction-create.json`
2. Vary: amount, payment_method, installments
3. Run multiple times with different data
4. Validate the results

### Test Full Flow

1. Create a customer → Copy the ID
2. Create a payment link → Copy the URL
3. Check the balance
4. List recent transactions

### Validate Recipients

1. Create a recipient → Copy the ID
2. List recipients
3. Update settings
4. Create a transfer using the recipient_id

## 📝 Conventions

- **Unique emails:** Vary the email on each creation
- **Valid IDs:** Use real IDs obtained from the API
- **Valid payloads:** Follow the official documentation structure

## 🔍 Debug

If you encounter errors:

1. **Check the JSON payload** — Correct syntax?
2. **Verify credentials** — Valid API key?
3. **Read the error message** — The API returns details
4. **Check the documentation** — https://docs.beehivehub.io/

## 📞 Support

- 📧 Email: support@paybeehive.com.br
- 📚 Docs: https://docs.beehivehub.io/
- 🐛 Issues: https://github.com/paybeehive/beehivehub-python-sdk/issues
- 📦 SDK: https://pypi.org/project/beehivehub-python-sdk/

---

✨ Built with ❤️ by the Beehive Hub team
