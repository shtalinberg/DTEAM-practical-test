# DTEAM - Django Developer Practical Test

Project Folder Structure
========================

```text
repo_root/                     # Project root directory
│── allstatic/                 # Collected static files
│── media/                     # Uploaded media files
│── volumes/                   # Docker volumes files
│── sc_backend/                # Main source code directory for backend
│   ├── djapps/                # All our Django applications
│   │   ├── audit/               # app audit
│   │   ├── core/                # app core
│   │   ├── cvsai/               # app cvsai -  CVs with AI
│   ├── djproject/             # Django project configuration (settings, URLs, etc.)
│   ├── manage.py
│── .gitignore
│── Makefile
│── README.md
│── ....
```

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
