from jinja2 import Environment, PackageLoader, select_autoescape

async def admin_loader() -> PackageLoader:
    """ Setup templating environment for """

    loader = PackageLoader("apps.admin", "templates"),

    return loader
