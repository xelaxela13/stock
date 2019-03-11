from django.urls import reverse_lazy
from admin_tools.dashboard import modules, AppIndexDashboard


class MyAppIndexDashboard(AppIndexDashboard):

    def __init__(self, app_title, models, **kwargs):
        AppIndexDashboard.__init__(self, app_title, models, **kwargs)

        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                limit=5
            ),
        ]
        if self.app_title == 'Склад':
            self.children.append(modules.LinkList(
                layout='inline',
                children=(
                    {
                        'title': 'Очистить кеш!',
                        'url': reverse_lazy('clear-cache'),
                        'external': False,
                        # 'description': 'Python language rocks !',
                        # 'attrs': {'target': '_blank'},
                    },
                )
            ))
