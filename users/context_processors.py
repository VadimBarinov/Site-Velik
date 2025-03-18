from catalog.utils import menu


def get_catalog_context(request):
    return {'main_menu': menu}
