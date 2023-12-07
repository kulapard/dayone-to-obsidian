import click


def echo_red(text: str) -> None:
    click.echo(click.style(text, fg="red"), err=True)


def echo_yellow(text: str) -> None:
    click.echo(click.style(text, fg="yellow"))


def echo_green(text: str) -> None:
    click.echo(click.style(text, fg="green"))
