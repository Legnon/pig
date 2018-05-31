# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import sys

try:
    from jinja2 import Template
    from termcolor import cprint
except ImportError:
    print('jinja2, termcolor 라이브러리가 필요합니다.', file=sys.stderr)
    sys.exit(1)


class Installer(object):
    def __init__(self, django_settings_module):
        self.project_root = os.path.abspath(os.path.dirname(__file__))              # django-dist.py의 상위폴더

        try:
            module = __import__(django_settings_module)
            for name in django_settings_module.split('.')[1:]:
                module = getattr(module, name)
            settings = module
        except ImportError as e:
            raise RuntimeError('IMPORT ERROR: {}'.format(e))

        self.req_path = os.path.join(self.project_root, 'req', 'prod.txt')
        self.kwargs = {
            'project_name': django_settings_module.split('.', 1)[0],                # PROJECT_NAME
            'project_root': self.project_root,
            'static_url_prefix': getattr(settings, 'STATIC_URL', '').rstrip('/'),   # static
            'static_root': getattr(settings, 'STATIC_ROOT', ''),                    # staticfiles
            'media_url_prefix': getattr(settings, 'MEDIA_URL', '').rstrip('/'),     # media
            'media_root': getattr(settings, 'MEDIA_ROOT', ''),                      # media
            'django_settings_module': django_settings_module,                       # PROJECT_NAME.settings.prod
            'db_engine': settings.DATABASES['default']['ENGINE'],                   # postgresql
            'db_host': settings.DATABASES['default'].get('HOST', ''),
            'db_name': settings.DATABASES['default']['NAME'],
            'db_user': settings.DATABASES['default'].get('USER', ''),
            'db_password': settings.DATABASES['default'].get('PASSWORD', ''),
        }

        if not self.kwargs['static_url_prefix']:
            raise RuntimeError('{}.STATIC_URL 을 설정해주세요. ex) "/static/"'.format(django_settings_module))

        if not self.kwargs['static_root']:
            raise RuntimeError('{}.STATIC_ROOT 를 설정해주세요. ex) os.path.join(BASE_DIR, "..", "staticfiles")'.format(django_settings_module))

        if not self.kwargs['media_url_prefix']:
            raise RuntimeError('{}.MEDIA_URL 을 설정해주세요. ex) "/media/"'.format(django_settings_module))

        if not self.kwargs['media_root']:
            raise RuntimeError('{}.MEDIA_ROOT 를 설정해주세요. ex) os.path.join(BASE_DIR, "..", "media")'.format(django_settings_module))

        if os.environ['USER'] != 'root':
            raise RuntimeError('root 권한으로 실행해주세요.')

        if not os.path.exists('/etc/apt/sources.list.d/'):
            raise RuntimeError('ubuntu os 만을 지원합니다.')

        if not os.path.exists(os.path.join(self.project_root, 'manage.py')):
            raise RuntimeError('django project root 로 옮겨주세요.')

        if not os.path.exists(self.req_path):
            raise RuntimeError('req/prod.txt 를 생성해주세요.')

        if ('psycopg2' not in self.kwargs['db_engine']) and ('postgis' not in self.kwargs['db_engine']):
            raise RuntimeError('PostgreSQL 데이터베이스만 지원합니다.')

    def run(self, service_only="True"):
        if service_only == "True":
            self.install_python_packages()
            self.init_django_project()
            self.init_nginx()
            self.init_uwsgi()
            self.service_start()
        else:
            self.init_apt()
            self.install_system_packages()
            self.init_db()
            self.install_python_packages()
            self.make_logs_directory()
            self.init_django_project()
            self.init_nginx()
            self.init_uwsgi()
            self.service_start()

    def init_apt(self):
        'Ubuntu 14.04 에서는 PostgreSQL 9.3 이 설치되므로, 상위버전을 설치하기 위한 추가 세팅'

        APT_PGDG_PATH = '/etc/apt/sources.list.d/pgdg.list'
        if not os.path.exists(APT_PGDG_PATH):
            with open(APT_PGDG_PATH, 'a', encoding='utf8') as f:
                f.write('\n')
                f.write('deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main')
            self.command_run('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')

    def install_system_packages(self):
        '시스템 팩키지 설치'

        self.command_run('''
            sudo apt-get update && \
            sudo apt-get install -y git python3-pip python3-dev \
                libpq-dev postgresql postgresql-contrib \
                nginx \
                libjpeg8-dev zlib1g-dev \
                libpcre3 libpcre3-dev
        ''')

    def init_db(self):
        'Django 프로젝트 데이터베이스/계정 생성 및 암호 설정'

        if 'psycopg2' in self.kwargs['db_engine']:
            for key in ('db_host', 'db_name', 'db_user', 'db_password'):
                if not self.kwargs[key]:
                    raise RuntimeError('{} 설정을 해주세요.'.format(key))

            if self.kwargs['db_host'] == '127.0.0.1':
                # peer
                self.command_run('''
                    sudo -u postgres dropdb --if-exists {db_name}
                    sudo -u postgres dropuser --if-exists {db_user}
                    sudo -u postgres createdb {db_name} && \
                    sudo -u postgres createuser {db_user} && \
                    echo "ALTER ROLE {db_user} WITH PASSWORD '{db_password}';" | sudo -u postgres psql
                ''')
            else:
                self.command_run('''
                    sudo -u postgres dropdb --if-exists --host={db_host} {db_name}
                    sudo -u postgres dropuser --if-exists --host={db_host} {db_user}
                    sudo -u postgres createdb --host={db_host} {db_name} && \
                    sudo -u postgres createuser --host={db_host} {db_user} && \
                    echo "ALTER ROLE {db_user} WITH PASSWORD '{db_password}';" | sudo -u postgres psql --host={db_host}
                ''')

    def install_python_packages(self):
        'Django 프로젝트, 파이썬 팩키지 설치'
        # req = open(self.req_path, 'r').readlines()
        # if 'pillow\n' in req or 'Pillow\n' in req:
        #     self.command_run('sudo apt-get install zlib1g-dev')

        self.command_run('sudo pip3 install -r {}'.format(self.req_path))

    def make_logs_directory(self):
        'Django 프로젝트 로그 디렉토리 생성'

        self.command_run('''
            sudo mkdir -p /var/log/{project_name} && \
            sudo chown www-data:www-data /var/log/{project_name}
        ''')

    def init_django_project(self):
        self.command_run('''
            python3 manage.py collectstatic --noinput --settings={django_settings_module} && \
            python3 manage.py makemigrations --settings={django_settings_module} && \
            python3 manage.py migrate --settings={django_settings_module}
        ''')

    def init_nginx(self):
        self.command_run('''
            sudo mkdir -p {media_root} && \
            sudo chown www-data:www-data {media_root}
        ''')

        config = Template(self.NGINX_CONFIG_TEMPLATE).render(**self.kwargs)
        open('/etc/nginx/nginx.conf', 'w', encoding='utf8').write(config)

    def init_uwsgi(self):
        config = Template(self.UWSGI_CONFIG_TEMPLATE).render(**self.kwargs)
        open('/etc/init/{project_name}.conf'.format(**self.kwargs), 'w', encoding='utf8').write(config)
        config = Template(self.UWSGI_INI_TEMPLATE).render(**self.kwargs)
        open('{project_root}/{project_name}.ini'.format(**self.kwargs), 'w', encoding='utf8').write(config)

    def service_start(self):
        self.command_run('''
            sudo service {project_name} restart && \
            sudo service nginx restart
        ''')

    def command_run(self, command):
        if isinstance(command, (list, tuple)):
            command = '\n'.join(command)

        command = command.format(**self.kwargs)

        print()
        for line in command.splitlines():
            line = ' '.join(line.strip().split())
            cprint(line, 'green', attrs=['bold'])
        print()
        result = os.system(command)
        if result != 0:
            raise RuntimeError('명령 수행 실패, result = {}'.format(result))

    NGINX_CONFIG_TEMPLATE = '''
user www-data;
worker_processes 1;
pid /run/nginx.pid;
events {
    worker_connections 1024;
}
http {
    sendfile on;
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
    server {
        listen 80;
        client_max_body_size 3M;
        keepalive_timeout 5;
        root {{ project_root }};
        access_log /var/log/{{ project_name }}/nginx_access.log main;
        rewrite ^/robots.txt(/?)+$ /static/robots.txt last;
        location {{ static_url_prefix }} {
            expires   1m;
            autoindex off;
            alias     {{ static_root }};
        }
        location {{ media_url_prefix }} {
            expires   1m;
            autoindex off;
            alias     {{ media_root }};
        }
        location / {
            expires     epoch;
            include     uwsgi_params;
            uwsgi_pass  127.0.0.1:8080;
            uwsgi_param UWSGI_SCHEME $scheme;
        }
    }
}
'''

    UWSGI_CONFIG_TEMPLATE = '''
description "{{ project_name }} uwsgi service"
start on runlevel [2345]
stop on runlevel [016]
script
    uwsgi --ini {{ project_root }}/{{ project_name }}.ini
end script
'''

    UWSGI_INI_TEMPLATE = '''
[uwsgi]
module = wsgi:application

master = true
processes = 1
die-on-term = true
enable-threads = true

socket = :8080
reload-on-rss = 100
harakiri = 30
harakiri-verbose = true

wsgi-file = {{ project_root }}/{{ project_name }}/wsgi_prod.py
pythonpath = {{ project_root }}

logto = /var/log/{{ project_name }}/uwsgi.log

uid = www-data
gid = www-data
'''


if __name__ == '__main__':
    try:
        django_settings_module = sys.argv[1]
    except IndexError:
        cprint('Usage) {} <django_settings_module>'.format(sys.argv[0]), 'red', file=sys.stderr)
        sys.exit(1)

    try:
        Installer(django_settings_module).run(sys.argv[2])
    except IndexError:
        Installer(django_settings_module).run()
    except RuntimeError as e:
        cprint('Error) {}'.format(e), 'red', file=sys.stderr)
        sys.exit(1)

