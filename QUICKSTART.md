# Quick Start

## 1. Clone and install

```bash
git clone https://github.com/paybeehive/beehivehub-python-sdk-runner.git
cd beehivehub-python-sdk-runner
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -e .
```

## 2. Configure

```bash
cp .env.example .env
```

Edit `.env` and set your API key:

```
BEEHIVE_SECRET_KEY=sk_live_your_key_here
BEEHIVE_ENVIRONMENT=sandbox
```

## 3. Run

```bash
python -m src.cli
```

## 4. Navigate

Use arrow keys to select a resource and operation. The CLI will guide you through each step.

## Tips

- All API responses are saved automatically in the `output/` folder
- Customize request payloads by editing JSON files in `payloads/`
- Use `Ctrl+C` to exit at any time
- IDs from previous operations can be used in subsequent ones (e.g., create a customer, then use the returned ID to create a transaction)
