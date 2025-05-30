# molecule/default/tests/test_default.py
puma_name = "puma"
puma_user = "deploy"
puma_config_dir = "/etc/puma"
puma_config_file = "/etc/puma/puma.rb"
puma_dir = "/var/www/html"
puma_bind = "unix:///var/www/html/puma.sock"
puma_pidfile = "/var/www/html/puma.pid"
puma_state_path = "/var/www/html/puma.state"
puma_activate_control_app = "unix:///var/www/html/pumactl.sock"
puma_systemd_unit_type = "service"
puma_systemd_unit_file = f"/etc/systemd/system/{puma_name}.{puma_systemd_unit_type}"
puma_systemd_service_name = "puma"


def test_puma_config_dir_exists(host):
    puma = host.file(puma_config_dir)
    assert puma.exists, f"{puma_config_dir} does not existh"
    assert puma.is_directory, f"{puma_config_dir} is not a directory"
    assert puma.user == puma_user, f"{puma_config_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_config_dir} group is not {puma_user}"
    assert puma.user == puma_user, f"{puma_config_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_config_dir} group is not {puma_user}"


def test_puma_config_file_exists(host):
    config = host.file(puma_config_file)
    assert config.exists, f"{puma_config_file} does not exist"
    assert config.is_file, f"{puma_config_file} is not a file"
    assert config.user == puma_user, f"{puma_config_file} is not owned by {puma_user}"
    assert config.group == puma_user, f"{puma_config_file} group is not {puma_user}"

    content = config.content_string
    assert f'directory "{puma_dir}"' in content
    assert f'bind "{puma_bind}"' in content
    assert f'pidfile "{puma_pidfile}"' in content
    assert f'state_path "{puma_state_path}"' in content
    assert (
        f'activate_control_app "{puma_activate_control_app}", {{ no_token: true }}'
        in content
    )


def test_puma_systemd_unit_file_contents(host):
    f = host.file(puma_systemd_unit_file)
    content = f.content_string
    assert "[Unit]" in content
    assert "Description=Puma web server" in content
    assert "After=network.target" in content
    assert "[Service]" in content
    assert "ExecStart = /usr/local/bin/puma -C /etc/puma/puma.rb" in content
    assert "ExecStop = /usr/local/bin/pumactl -F /etc/puma/puma.rb stop" in content
    assert (
        "ExecReload = /usr/local/bin/pumactl -F /etc/puma/puma.rb phased-restart"
        in content
    )
    assert "User = deploy" in content
    assert "Group = deploy" in content
    assert "WorkingDirectory = /var/www/html" in content
    assert "Restart = always" in content
    assert "[Install]" in content
    assert "WantedBy=multi-user.target" in content


def test_puma_service_is_enabled(host):
    svc = host.service(puma_systemd_service_name)
    assert svc.is_enabled


def test_puma_service_is_running(host):
    svc = host.service(puma_systemd_service_name)
    assert svc.is_running
