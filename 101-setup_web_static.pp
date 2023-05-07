# Puppet to configure server for deployment

$config_nginx = "server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location /hbnb_static {
                alias /data/web_static/current/;
        }
        location /redirect_me{
                return 301 http://www.google.com;
        }
        error_page 404 /404.html;
        location = /404.html {
                root /usr/share/nginx/html;
                internal    ;
        }

        location / {
                add_header X-Served-By ${hostname};
                try_files ${uri} ${uri}/ =404;
        }
}"

$simple_html = "<html>
  <head>
  </head>
  <body>
    ALX School
  </body>
</html>"

exec { 'update':
    command => '/usr/bin/apt-get update -y',
}

-> package { 'nginx':
    ensure  => installed,
    require => Exec['update']
}

-> file { '/data':
  ensure  => 'directory'
}

-> file { '/data/web_static':
  ensure => 'directory'
}

-> file { '/data/web_static/releases':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test':
  ensure => 'directory'
}

-> file { '/data/web_static/shared':
  ensure => 'directory'
}

-> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => $simple_html
}

-> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => 'yes'
}

-> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/'
}

-> file { '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => $config_nginx
}

-> service { 'nginx':
  ensure => 'running',
}
