# stock
Nginx example:
```
server {
    listen      localhost:80;
    server_name DOMAIN www.DOMAIN;
    error_log  /var/log/httpd/domains/DOMAIN.error.log error;

    location / {
        proxy_pass      http://localhost:8001;
        location ~* ^.+\.(jpeg|jpg|png|gif|bmp|ico|svg|tif|tiff|css|js|htm|html|ttf|otf|webp|woff|txt|csv|rtf|doc|docx|xls|xlsx|ppt|pptx|odf|odp|ods|odt|pdf|psd|ai|eot|eps|
            root           /home/USER/web/DOMAIN/public_shtml;
            access_log     /var/log/httpd/domains/DOMAIN.log combined;
            access_log     /var/log/httpd/domains/DOMAIN.bytes bytes;
            expires        max;
            try_files      $uri @fallback;
        }
    }

    location /error/ {
        alias   /home/USER/web/DOMAIN/document_errors/;
    }

    location @fallback {
        proxy_pass      http://localhost:8001;
    }
    
    location /static {
        autoindex on;
        alias /home/USER/web/DOMAIN/public_shtml/static_content/asset;
    }
    location /media {
        autoindex on;
        alias /home/USER/web/DOMAIN/public_shtml/static_content/media;
    }
    location ~ /\.ht    {return 404;}
        location ~ /\.svn/  {return 404;}
        location ~ /\.git/  {return 404;}
        location ~ /\.hg/   {return 404;}
        location ~ /\.bzr/  {return 404;}
    
        if ($host ~* ^www\.(.*)$) {
           rewrite / $scheme://$1 permanent;
        }
    include /home/USER/conf/web/nginx.DOMAIN.conf*;
}

server {
    listen      localhost:443;
    server_name DOMAIN www.DOMAIN;
    ssl         on;
    ssl_certificate      /home/USER/conf/web/ssl.DOMAIN.pem;
    ssl_certificate_key  /home/USER/conf/web/ssl.DOMAIN.key;
    error_log  /var/log/httpd/domains/DOMAIN.error.log error;

    location / {
        proxy_pass      http://localhost:8444;
        location ~* ^.+\.(jpeg|jpg|png|gif|bmp|ico|svg|tif|tiff|css|js|htm|html|ttf|otf|webp|woff|txt|csv|rtf|doc|docx|xls|xlsx|ppt|pptx|odf|odp|ods|odt|pdf|psd|ai|eot|eps|
            root           /home/USER/web/DOMAIN/public_shtml;
            access_log     /var/log/httpd/domains/DOMAIN.log combined;
            access_log     /var/log/httpd/domains/DOMAIN.bytes bytes;
            expires        max;
            try_files      $uri @fallback;
        }
    }
        
    location /error/ {
        alias   /home/USER/web/DOMAIN/document_errors/;
    }

    location @fallback {
        proxy_pass      http://localhost:8444;
    }
    location /static {
        autoindex on;
        alias /home/USER/web/DOMAIN/public_shtml/static_content/asset;
    }
    location /media {
        autoindex on;
        alias /home/USER/web/DOMAIN/public_shtml/static_content/media;
    }
    location ~ /\.ht    {return 404;}
        location ~ /\.svn/  {return 404;}
        location ~ /\.git/  {return 404;}
        location ~ /\.hg/   {return 404;}
        location ~ /\.bzr/  {return 404;}

    include /home/USER/conf/web/snginx.DOMAIN.conf*;
}













