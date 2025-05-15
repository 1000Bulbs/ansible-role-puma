# Ansible Role: okb.puma

[![CI](https://github.com/1000Bulbs/ansible-role-puma/actions/workflows/ci.yml/badge.svg)](https://github.com/1000Bulbs/ansible-role-puma/actions/workflows/ci.yml)

A brief description of the role goes here.

---

## ✅ Requirements

- Ansible 2.13+
- Python 3.9+ (for Molecule + testinfra)
- Tested on Ubuntu 22.04+

---

## ⚙️ Role Variables

These variables can be overridden in your inventory, playbooks, or `group_vars`.

### Defaults (`defaults/main.yml`)

Add a list of default variables that are defined in the role's `defaults/main.yml` file.

### Variables (`vars/main.yml`)

_No variables defined._

---

## 📦 Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be
set for other roles, or variables that are used from other roles.

---

## 📥 Installing the Role

To include this role in your project using a `requirements.yml` file:

```yaml
roles:
  - name: okb.puma
    src: git@github.com:1000bulbs/ansible-role-puma.git
    scm: git
    version: master
```

Then install it with:

```bash
ansible-galaxy role install -r requirements.yml
```

---

## 💡 Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for
users too:

```yaml
- name: My Playbook
  hosts: all
  become: true
  roles:
    - role: okb.puma
```

---

## 🧪 Testing

This role uses a `Makefile` for linting and formatting, and [Molecule](https://molecule.readthedocs.io/) with
`pytest-testinfra` for integration testing.

### Run tests locally

#### Lint and Format

```bash
# Run all checks (linting and formatting)
make check

# Run linting tools manually (ruff, yamllint, ansible-lint)
make lint

# Run Python formatting tools manually (ruff)

make format
```

#### Integration Tests

Install dependencies

```bash
pip install -r requirements.txt
```

Run Molecule integration tests

```bash
molecule test
```

---

## 🪝 Git Hooks

This project includes [pre-commit](https://pre-commit.com/) integration via Git hooks to automatically run formatting and linting checks **before each commit**.

These hooks help catch errors early and keep the codebase consistent across contributors.

### Install Git Hooks

```bash
make install-hooks
```

This will:

- Install pre-commit (if not already installed)
- Register a Git hook in .git/hooks/pre-commit
- Automatically run checks like:
- Code formatting with black and isort
- Linting with ruff, yamllint, and ansible-lint

### Remove Git Hooks

```bash
make uninstall-hooks
```

This removes the Git pre-commit hook and disables automatic checks.

💡 Even with hooks uninstalled, you can still run the same checks manually with `make test`.

Why Use Git Hooks?

- Ensures consistency across contributors
- Catches syntax and style issues before they hit CI
- Prevents accidental commits of broken or misformatted files
- Integrates seamlessly with your local workflow
