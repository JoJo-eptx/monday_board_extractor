# Monday Board Extractor

A Python package to extract data from Monday.com boards and convert it into pandas DataFrames.

## Installation

To install the package locally, clone or download this repository and run the following command from the project root directory:

```powershell
pip install .
```

For development (editable) mode, use:

```powershell
pip install -e .
```

## Usage Example

```python
from monday_board_extractor import MondayColumnExtractor
import yaml
from pathlib import Path

# Load API key from config file in the project root
yaml_path = Path.cwd() / "monday_config.yaml"
with yaml_path.open("r") as f:
    config = yaml.safe_load(f)
api_key = config["monday"]["api_key"]

# Specify board IDs to extractoard_ids = [123456789]

# Create extractor and extract data
extractor = MondayColumnExtractor(api_key, board_ids)
results = extractor.extract()

# Print board names and data
for board_data in results:
    print(board_data.name)
    print(board_data.data.head())
```

## Requirements
- requests
- pandas
- pyyaml

Install requirements with:
```powershell
pip install -r requirements.txt
```

## License
MIT
