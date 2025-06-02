from jinja2 import Environment, PackageLoader, select_autoescape

async def trip_loader() -> Environment:
    """ Setup templating environment for trips """

    loader = PackageLoader("apps.trip", "templates")

    return loader
