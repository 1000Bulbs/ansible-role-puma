# molecule/default/tests/test_puma.py
from utils import load_yaml

vars = load_yaml("../vars/all.yml")

puma_dir = vars["puma_dir"]
puma_user = vars["puma_user"]


def test_puma_dir_exists(host):
    puma = host.file(puma_dir)
    assert puma.exists, f"{puma_dir} does not exist"
    assert puma.is_directory, f"{puma_dir} is not a directory"
    assert puma.user == puma_user, f"{puma_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_dir} group is not {puma_user}"
    assert puma.user == puma_user, f"{puma_dir} is not owned by {puma_user}"
    assert puma.group == puma_user, f"{puma_dir} group is not {puma_user}"
