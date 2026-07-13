from .views import MODULES_CONFIG


def module_links(request):
    return {
        'module_links': [
            {'name': key, 'label': config['label']}
            for key, config in MODULES_CONFIG.items()
        ]
    }
