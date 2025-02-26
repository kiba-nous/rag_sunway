# Setup Instructions

## Virtual Environment Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   **On Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

   **On Windows:**
   ```bash
   .\venv\Scripts\activate
   ```

3. Upgrade pip:
   ```bash
   pip install -U pip
   ```

## Jupyter Notebook Setup

1. Install ipykernel (if not already installed):
   ```bash
   pip install ipykernel
   ```

2. Register your virtual environment with Jupyter:
   ```bash
   python -m ipykernel install --user --name=venv --display-name="Python (venv)"
   ```

3. Select the kernel in your Jupyter notebook:
   * Launch Jupyter Notebook
   * Open your notebook
   * Click on "Kernel" in the top menu
   * Select "Change kernel"
   * Choose "Python (venv)" from the dropdown menu

4. Now you can install and use dependencies within your virtual environment.

## Troubleshooting

- If your kernel doesn't appear in the list, restart Jupyter Notebook
- To verify your virtual environment is active, check for `(venv)` at the beginning of your command prompt
- To deactivate your virtual environment, simply run `deactivate`