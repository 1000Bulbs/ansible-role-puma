# Ansible Role: puma

[![CI](https://github.com/1000Bulbs/ansible-role-puma/actions/workflows/ci.yml/badge.svg)](https://github.com/1000Bulbs/ansible-role-puma/actions/workflows/ci.yml)

This role automates the setup and management of the Puma web server for Ruby on Rails applications on Ubuntu systems.

- Installs and configures the Puma application server for Ruby on Rails apps.
- Sets up a systemd service to manage the Puma process.
- Generates a `puma.rb` config file using a customizable Ansible template.
- Ensures directory structure and file ownerships for Puma logs, PID, and sockets.

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

```yaml
# Puma name
puma_name: puma

# System user that will run the Puma process
puma_user: deploy

# Directory where Puma configuration is stored
puma_config_dir: /etc/puma

# File where Puma configuration is stored
puma_config_file: "{{ puma_config_dir }}/puma.rb"

# Root directory of the deployed Rails application
puma_dir: /var/www/html

# The environment in which Puma will run (e.g., development, staging, production)
puma_env: production

# Whether to enable preload_app! in the Puma config for Copy-On-Write memory savings
puma_preload_app_enabled: true

# Number of Puma worker processes.
# Leave blank to have this set automatically based on the number of server CPUs.
puma_workers: "{{ ((ansible_processor_vcpus // 2) | int) if ansible_processor_vcpus > 1 else 1 }}"

# Number of threads per Puma worker.
# Leave blank to have this set automatically based on the number of server CPUs.
puma_threads: "{{ (puma_workers | int) + 1 }}"

# The socket that Puma will bind to for accepting requests
puma_bind: unix://{{ puma_dir }}/puma.sock

# File where Puma will write its PID (process ID)
puma_pidfile: "{{ puma_dir }}/puma.pid"

# File where Puma will store its state (for use with phased restarts, etc.)
puma_state_path: "{{ puma_dir }}/puma.state"

# Whether to enable Puma's control app for phased restarts and monitoring
puma_activate_control_app_enabled: true

# Path to Puma's control socket for pumactl commands
puma_activate_control_app: unix://{{ puma_dir }}/pumactl.sock

# Token used to authenticate requests to the Puma control app
puma_activate_control_app_token: "no_token: true"

# File where Puma will write standard log output
puma_log_file: "{{ puma_dir }}/log/puma.log"

# File where Puma will write error log output
puma_error_log_file: "{{ puma_dir }}/log/puma-error.log"

# Whether to enable `prune_bundler` to clean up unused gem references after a restart
puma_prune_bundler_enabled: true

# Type of the systemd unit.
puma_systemd_unit_type: service

# Default directory for systemd unit files.
puma_systemd_unit_directory: /etc/systemd/system

# Full path for the systemd unit file, constructed using the directory, unit name, and type.
puma_systemd_unit_file: "{{ puma_systemd_unit_directory }}/{{ puma_name }}.{{ puma_systemd_unit_type }}"

# Generic options for systemd units, applied regardless of the unit type.
puma_systemd_unit_generic_options:
  - Description=Puma web server
  - After=network.target

# Path to the Puma executable binary
puma_binary: /usr/local/bin/puma

# Command to start Puma via systemd unit
puma_systemd_unit_exec_start: "{{ puma_binary }} -C {{ puma_config_file }}"

# Path to the pumactl control utility binary
puma_ctl_binary: /usr/local/bin/pumactl

# Command to stop Puma via systemd unit
puma_systemd_unit_exec_stop: "{{ puma_ctl_binary }} -F {{ puma_config_file }} stop"

# Command to reload (restart) Puma via systemd unit
puma_systemd_unit_exec_reload: "{{ puma_ctl_binary }} -F {{ puma_config_file }} phased-restart"

# Restart policy for the Puma systemd unit
puma_systemd_unit_restart: always

# Specific options for the systemd unit, dependent on the unit type and configuration.
puma_systemd_unit_options:
  - Type = simple
  - ExecStart = {{ puma_systemd_unit_exec_start }}
  - ExecStop = {{ puma_systemd_unit_exec_stop }}
  - ExecReload = {{ puma_systemd_unit_exec_reload }}
  - User = {{ puma_user }}
  - Group = {{ puma_user }}
  - WorkingDirectory = {{ puma_dir }}
  - Restart = {{ puma_systemd_unit_restart }}
  - PIDFile = {{ puma_pidfile }}

# Options related to the 'Install' section of a systemd unit file.
puma_systemd_unit_install_options:
  - WantedBy=multi-user.target

  # Name of the systemd service.
puma_systemd_service_name: "{{ puma_name }}"

# Whether or not the systemd service is enabled.
puma_systemd_service_enabled: true

# The systemd service state.
puma_systemd_service_state: started
```

### Variables (`vars/main.yml`)

_No variables defined._

---

## 📦 Dependencies

No external roles or collections required.

---

## 📥 Installing the Role

To include this role in your project using a `requirements.yml` file:

```yaml
roles:
  - name: okb.puma
    src: https://github.com/1000bulbs/ansible-role-puma.git
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
- name: Puma web server
  hosts: all
  become: true
  roles:
    - role: okb.puma
```

---

## 🧪 Testing

This role uses Python and Node.js for linting and formatting, Molecule with pytest-testinfra for integration testing,
and Act for local GitHub Actions testing — all orchestrated through a Makefile for ease of use and convenience.

### Install dependencies

Install all dependencies and setup environment

```bash
make setup
```

### Run tests locally

#### Lint and Format Checks

Run lint and format checks

```bash
make check
```

#### Integration Tests

Run integration tests

```bash
make test
```

#### GitHub Actions Tests

Run github actions tests locally

```bash
make ci
```

---

## 🪝 Git Hooks

This project includes [pre-commit](https://pre-commit.com/) integration via Git hooks to automatically run formatting and linting checks **before each commit**.

These hooks help catch errors early and keep the codebase consistent across contributors.

### Prerequisites

Before installing the hooks, make sure your system has:

- **Python 3.9+** with `pip` installed
- **Node.js** and `npm` (required for `markdownlint-cli2`)

You can check your versions with:

```bash
python3 --version
pip --version
node --version
npm --version
```

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

### Test Git Hooks

```bash
make test-hooks
```

This will run the pre-commit hooks on all files, the same as when you run `git commit`.

### Remove Git Hooks

```bash
make uninstall-hooks
```

This removes the Git pre-commit hook and disables automatic checks.

💡 Even with hooks uninstalled, you can still run the same checks manually with `make test-hooks`.

Why Use Git Hooks?

- Ensures consistency across contributors
- Catches syntax and style issues before they hit CI
- Prevents accidental commits of broken or misformatted files
- Integrates seamlessly with your local workflow
