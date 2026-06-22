# Supermarket Ads Agent

> A stock-aware promotional ad-copy agent. It reads live inventory and pricing
> from a store's stock spreadsheet, selects products with healthy margin and
> visible discount, and prepares them for promotional ad generation.

## What it does

`parser.py` loads a "Stock Summary" sheet (header on the 3rd row), normalises
the messy column names, coerces the numeric columns (MRP, selling price,
quantity), and selects a shortlist of products that satisfy the thresholds in
[`config.json`](config.json) — minimum margin, minimum visible discount, and a
cap on how many products to advertise at once.

It is designed to run as the Python step inside a self-hosted
[n8n](../n8n/) workflow, which handles scheduling, approval, and delivery.

## Configuration

`config.json` holds the tunable parameters (no secrets):

| Key | Meaning |
|-----|---------|
| `store_name` | Display name used in generated copy |
| `excel_path` | Path to the stock spreadsheet |
| `max_products` | Cap on products advertised per run |
| `min_margin_pct` | Minimum margin to qualify a product |
| `min_visible_discount_pct` | Minimum advertised discount |
| `approval_email` | Where the approval request is sent |

## Run

Managed with [uv](https://github.com/astral-sh/uv).

```bash
cd automation/supermarket-ads
uv sync

# Point PRODUCT_XLSX_PATH at your stock sheet (defaults to ./product.xlsx)
PRODUCT_XLSX_PATH=/path/to/product.xlsx uv run python parser.py
```

The spreadsheet is environment-specific and is not committed.
