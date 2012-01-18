from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from os import path, system, listdir, remove

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option('--Version', '-V', default='1.0',
                help='Version number'),
    )

    help = 'Collects static files and minimizes js and css scripts'

    def handle(self, *args, **options):
        def is_min(file_name):
            name, ext = path.splitext(file_name)
            name, ext = path.splitext(name)
            return ext == '.min'

        ver = options.get('Version')

        cmd_js = 'yui-compressor --type js '
        cmd_css = 'yui-compressor --type css '

        path_js = path.join(settings.STATIC_ROOT, 'js')
        path_css = path.join(settings.STATIC_ROOT, 'css')

        # not too nice?
        system('cd ' + settings.SETTINGS_DIR)
        system('python manage.py collectstatic --noinput')

        for js_file in listdir(path_js):
            name, ext = path.splitext(js_file)
            output = path.join(path_js, name + '-' + ver + '.min' + ext)
            old_file = path.join(path_js, js_file)
            if not is_min(old_file):
                system(cmd_js + '-o ' + output + ' ' + old_file)
                remove(old_file)

        for css_file in listdir(path_css):
            name, ext = path.splitext(css_file)
            output = path.join(path_css, name + '-' + ver + '.min' + ext)
            old_file = path.join(path_css, css_file)
            if not is_min(old_file):
                system(cmd_css + '-o ' + output + ' ' + old_file)
                remove(old_file)
