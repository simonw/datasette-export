from datasette.cli import cli
from click.testing import CliRunner
import pathlib
import pytest
import sqlite3


def test_plugin_is_installed(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Create a minimal database file
        conn = sqlite3.connect("data.db")
        conn.execute("create table t (x)")
        conn.execute("insert into t (x) values (1)")
        conn.close()
        result = runner.invoke(cli, ["export", "data.db", "--path", "/.json"])
        assert result.exit_code == 0, result.output
        files = list(pathlib.Path(td).glob("export/**/*"))
        relative_paths = [
            str(f.relative_to(pathlib.Path(td) / "export")) for f in files
        ]
        assert relative_paths == ["index.json"]
