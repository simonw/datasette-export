import asyncio
import click
import pathlib
from datasette import hookimpl


# These options do not work with 'datasette export':
invalid_options = {
    "get",
    "root",
    "open_browser",
    "uds",
    "reload",
    "pdb",
    "ssl_keyfile",
    "ssl_certfile",
}


def serve_with_export(**kwargs):
    from datasette import cli

    paths = kwargs.pop("paths")
    sqls = kwargs.pop("sqls")
    output = kwargs.pop("output")
    crossdb = kwargs.get("crossdb", False)

    out_dir = pathlib.Path(output)

    # Need to add back default kwargs for everything in invalid_options:
    kwargs.update({invalid_option: None for invalid_option in invalid_options})
    kwargs["return_instance"] = True
    ds = cli.serve.callback(**kwargs)

    def save(path, content):
        if path == "/":
            path = "index.html"
        if path == "/.json":
            path = "index.json"
        if "." not in path.split("/")[-1]:
            path = path + ".html"
        path = path.lstrip("/")
        if path.endswith("/"):
            path = path + "index.html"
        click.echo(path, err=True)
        out_path = out_dir / path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content)

    async def go():
        for path in paths:
            response = await ds.client.get(path)
            save(path, response.text)

        db = ds.get_database("_memory" if crossdb else None)
        for sql in sqls:
            print(sql)
            print()
            rows = await db.execute(sql)
            for row in rows:
                path = row[0]
                response = await ds.client.get(path)
                save(path, response.text)

    asyncio.run(go())


@hookimpl
def register_commands(cli):
    serve_command = cli.commands["serve"]
    params = [
        param for param in serve_command.params if param.name not in invalid_options
    ]
    params.extend(
        [
            click.Option(
                ["paths", "--path"],
                multiple=True,
                help="Path to export",
            ),
            click.Option(
                ["sqls", "--sql"],
                multiple=True,
                help="SQL query returning paths to export",
            ),
            click.Option(
                ["--output"],
                help="Output directory",
                default="export",
                type=click.Path(file_okay=False, dir_okay=True, writable=True),
            ),
        ]
    )
    export_command = click.Command(
        name="export",
        params=params,
        callback=serve_with_export,
        short_help="Export static files using Datasette",
    )
    cli.add_command(export_command, name="export")
