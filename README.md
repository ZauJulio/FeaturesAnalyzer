# Features Analyzer

![Static Badge](https://img.shields.io/badge/python-3.12-%233776AB?logo=Python&logoColor=white)
![Static Badge](https://img.shields.io/badge/pyenv-%2323478B?logo=python&logoColor=white)
![Static Badge](https://img.shields.io/badge/poetry-%236C5CE7?logo=poetry&logoColor=white)
![Static Badge](https://img.shields.io/badge/pandas-%23150458?logo=pandas&logoColor=white)
![Static Badge](https://img.shields.io/badge/numpy-%23013243?logo=numpy&logoColor=white)
![Static Badge](https://img.shields.io/badge/gtk-%2300D084?logo=gtk&logoColor=white)
![Static Badge](https://img.shields.io/badge/matplotlib-%23D62728?logo=python&logoColor=white)
![Static Badge](https://img.shields.io/badge/seaborn-%230098A4?logo=python&logoColor=white)
![Static Badge](https://img.shields.io/badge/pydantic-%231D3557?logo=pydantic&logoColor=white)
![Static Badge](https://img.shields.io/badge/i18n-%234CAF50?logo=googletranslate&logoColor=white)
![Static Badge](https://img.shields.io/badge/docker-%232496ED?logo=docker&logoColor=white)
![Static Badge](https://img.shields.io/badge/mkdocs-%23488CE8?logo=materialformkdocs&logoColor=white)
![Static Badge](https://img.shields.io/badge/pre--commit-enabled-%231F2E3A?logo=pre-commit&logoColor=white)
![Static Badge](https://img.shields.io/badge/renovate-enabled-%2300BBDE?logo=renovatebot&logoColor=white)

## Overview

This is a simple tool to analyze the features of a dataset, prototype and test machine learning/statistical models.
The project is built with Python type hints in all modules.

---

## Installation

<details>
<summary><strong>1. Prerequisites</strong></summary>

- **Python 3.12+**: Make sure you have Python 3.12 (or venv ;) ) or more recent installed on your system.
- **WSL (para Windows)**: Windows users should install the [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/pt-br/windows/wsl/install) to use Poetry.

</details>

---

<details>
<summary><strong>2. Install Poetry</strong></summary>

Poetry is used to manage dependencies and build the project. Follow the [link](https://python-poetry.org/docs/#installing-with-pipx) to install it or continue with to install with pyenv and pip.
</details>

---

<details>
<summary><strong>3. Install Project and Run</strong></summary>

### **With Poetry**

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the dependencies:

   ```bash
   poetry install
   ```

#### **With pyenv e pip**

1. Install Pyenv:

   ```bash
   curl https://pyenv.run | bash
   ```

2. Install and configure the Python version:

   ```bash
   pyenv install 3.12.0
   pyenv local 3.12.0
   ```

3. Install the facilities using the `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

#### **Docker**

1. The option to run via Docker is in its early stages and is a work in progress

   ```sh
   # If you are using X11, remember to allow the connection
   xhost +local:docker

   docker buildx build -t fa .

   # If u must use the local files, remember to map to volume
   docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --name fa fa
   ```

</details>

---

## Project Structure

- Basic

```txt
├── assets                              # Assets files
│   ├── styles                          # Global styles
│   └── icons                           # Icons
├── docs                                # Documentation used by MkDocs
├── i18n                                # Internationalization files
├── src                                 # Source code
│   ├── context                         # Context (Global state)
│   │   ├── states/*                    # States (With handlers)
│   │   └── store.py                    # Store/Merge context
│   ├── interfaces                      # Project interfaces
│   ├── models                          # Project models (extends FAModel)
│   ├── lib                             # Project libraries
│   │   ├── model_manager               # Model manager
│   │   ├── orm                         # Typed JSON ORM with Pydantic and tinydb
│   │   ├── state_manager               # State manager with Observer
│   │   ├── utils                       # Generic utils
│   │   └── widget.py                   # Generic Widget (extends Gtk.Widget)
│   └── sdk                             # SDKs for other services
├── .env.example                        # Environment variables example
└── requirements.txt                    # Python requirements file (alternative to poetry)
```

<details>
<summary>Advanced</summary>

```txt
├── assets                              # Assets files
│   ├── styles                          # Global styles
│   └── icons                           # Icons
├── docs                                # Documentation used by MkDocs
├── i18n                                # Internationalization files
├── src                                 # Source code
│   ├── context                         # Context (Global state)
│   │   ├── states/*                    # States (With handlers)
│   │   └── store.py                    # Store/Merge context
│   ├── interfaces                      # Project interfaces
│   ├── models/*                          # Project models (extends FAModel)
│   │   ├── application.py              # Global app interface
│   │   ├── controller.py               # Generic (handler and connect signals)
│   │   ├── module.py                   # Generic (handler root state signals)
│   │   ├── state.py                    # Generic State
│   │   └── widget.py                   # Generic Widget (extends Gtk.Widget)
│   ├── lib                             # Project libraries
│   │   ├── model_manager               # Model manager
│   │   ├── orm                         # Typed JSON ORM with Pydantic and tinydb
│   │   ├── state_manager               # State manager with Observer
│   │   ├── utils                       # Generic utils
│   │   │   ├── bin_.py                 # Binary models access
│   │   │   ├── hsash.py                # Hash utils
│   │   │   ├── lock.py                 # Lock utils to multiprocessing
│   │   │   ├── logger.py               # Global logger
│   │   │   ├── meta.py                 # Meta class utils (Singleton)
│   │   │   ├── time_.py                # T
│   │   │   ├── types_.py               # State manager with Observer
│   │   │   ├── ui.py                   # State manager with Observer
│   │   └── widget.py                   # Generic Widget (extends Gtk.Widget)
│   └── sdk                             # SDKs for other services
├── .editorconfig                       # Editor configuration
├── .env.example                        # Environment variables example
├── .gitignore                          # Git ignore file
├── .pre-commit-config.yaml             # Pre-commit configuration
├── Dockerfile                          # Dockerfile
├── Makefile                            # Makefile with common commands
├── poetry.lock                         # Poetry lock file
├── pyproject.toml                      # Python project file
├── requirements.txt                    # Python requirements file (alternative to poetry)
└── ruff.toml                           # Ruff (code linter/formatter) options
```

</details>

---

## Logic

- **Widget**: Interact with the user/screen
- **Controller**: Handle the widget state setter's/handle signals
- **Module**: Handle the controller with root state subscribes
- **Widget**: Integrate the module and interact with data/graphs, group widgets/modules, be creative ; )

---

## Tools Maintain Project

- [SonarCloud - Code Quality and Security](https://sonarcloud.io/project/overview?id=ZauJulio_FeaturesAnalyzer)
- [Renovate - Dependency Updates](https://developer.mend.io/github/ZauJulio/FeaturesAnalyzer)

---

## How to cite

```txt
@misc{zaujulioFeaturesAnalyzer,
  title={Features Analyzer},
  author={Zaú Júlio},
  year={2024},
  url={https://github.com/ZauJulio/FeaturesAnalyzer},
}
```

## Licença

UFRN/ZauJulio - 2024 💙🎓️
