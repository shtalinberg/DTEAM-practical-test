# DTEAM - Django Developer Practical Test

## Python Virtual Environment Setup

### Prerequisites
- Install pyenv
- Install Poetry

### Setting up the environment

1. **Install the required Python version using pyenv:**
   ```bash
   pyenv install 3.12.10
   ```

2. **Install Poetry dependencies:**
   ```bash
   poetry install
   ```

### Load cvsai app fixtures - initial data

   ```bash
   python sc_backend/manage.py loaddata cvsai_initial_data
   ```

### Run pytest tests

   ```bash
   cd sc_backend && pytest
   ```
or
   ```bash
   make pytest
   ```
