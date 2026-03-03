# NutriScan - Smart Snack Ingredient Analyzer

> A FOSS Hack project that scans snack labels, identifies ingredients, and tells you exactly what you're eating.

---

## What is NutriScan?

NutriScan is an open-source tool that lets you **scan the back of any snack or food product** using your camera. It automatically detects and extracts the ingredient list from the label, cross-references it against a curated nutritional dataset, and gives you a clear breakdown of:

- What ingredients are present
- Full nutritional information (calories, fats, sugar, sodium, etc.)
- Whether the product is **healthy or not**, based on standardized nutritional benchmarks

---

## How It Works

1. **Scan** - Take a photo or scan the back of a snack/food package
2. **Extract** - OCR reads and parses the ingredient list from the label
3. **Compare** - Extracted ingredients are matched against a nutritional dataset (Kaggle + internet sources)
4. **Analyze** - The system calculates nutritional values and flags harmful or unhealthy ingredients
5. **Report** - You get a simple, readable health verdict with full nutritional details

---

## Key Features

- Camera / image-based label scanning
- Automatic ingredient detection using OCR
- Ingredient-to-nutrition mapping via open datasets
- Nutritional summary (calories, sugar, fat, protein, additives, etc.)
- Health score / verdict: Healthy / Moderate / Unhealthy
- Highlights potentially harmful additives or allergens

---

## Tech Stack (Planned)

| Component | Technology |
|---|---|
| OCR / Image Processing | Tesseract OCR / OpenCV |
| Dataset | Kaggle Food Datasets / Open Food Facts |
| Backend | Python / FastAPI |
| Frontend | React / Flutter (TBD) |
| ML / NLP | spaCy / scikit-learn |

---

## Dataset Sources

- [Open Food Facts](https://world.openfoodfacts.org/) - Open-source food product database
- [Kaggle Food Datasets](https://www.kaggle.com/) - Community nutritional datasets
- Custom ingredient-nutrition mapping from publicly available sources

---

## Project Status

Currently in early development as part of **FOSS Hack**.

---

## Contributing

Contributions, dataset suggestions, and feature ideas are welcome! Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file.
