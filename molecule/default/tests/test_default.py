# molecule/default/tests/test_default.py
puma_config_dir = "/etc/puma"
puma_user = "deploy"


def test_puma_config_dir_exists(host):
    puma = host.file(puma_config_dir)
    assert puma.exists, f"{puma_config_dir} does not existh"
    assert puma.is_directory, f"{puma_config_dir} is not a directory"
    assert puma.user == puma_user, f"{puma_config_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_config_dir} group is not {puma_user}"
    assert puma.user == puma_user, f"{puma_config_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_config_dir} group is not {puma_user}"
