# thumbor_ftvnum_libs
Libs for thumbor

## Table of Contents
1. [General purposes] (#general)
2. [Loaders](#Loaders)
3. [Storages](#Storages)
4. [Result_storages](#Result_storages)
5. [Url_signers](#url_signers)
6. [FAQs](#faqs)



#general



# Loaders

1. [pic_nn_loader] (#pic_nn_loader)
2. [piv_nnh_loader] (#pic_nnh_loader)

## pic_nn_loader

Description: Loader de type file, avec un fallback sur une autre filesystem.

Implementation: 
```
LOADER = thumbor_ftvnum_libs.loaders.pic_nn_loader
```

Options:
```
PIC_LOADER_ROOT_PATH = #root path for file
PIC_LOADER_FALLBACK_PATH = #fallback path for file
PIC_LOADER_MAX_SIZE = #max size in bytes default 16777216
```

## pic_nnh_loader

Description: Loader de type pic_nn_loader, avec un fallback sur du http/s http_loader.

Implementation: 
```
LOADER = thumbor_ftvnum_libs.loaders.pic_nnh_loader
```

Options:
```
PIC_LOADER_ROOT_PATH = #root path for file
PIC_LOADER_FALLBACK_PATH = #fallback path for file
PIC_LOADER_MAX_SIZE = #max size in bytes default 16777216

#Ajouter les options additionnelles du LOADER http_loader standard
```

## mongodb_loader





# storages

## mongodb_webp_storage

Description: Stockage des images pour MongoDB/GridFS compatible avec la fonction auto_webp.

Implementation: 
```
STORAGE = thumbor_ftvnum_libs.storages.mongo_webp_storage
```

Options:
```
MONGO_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_STORAGE_SERVER_USER = '' # user
MONGO_STORAGE_SERVER_PASSWORD = '' # password
MONGO_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_STORAGE_SERVER_READ = 'secondaryPreferred'
```

## mongodb_storage

Description: Stockage des images pour MongoDB/GridFS (Legacy).

Implementation: 
```
STORAGE = thumbor_ftvnum_libs.storages.mongo_storage
```

Options:
```
MONGO_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_STORAGE_SERVER_USER = '' # user
MONGO_STORAGE_SERVER_PASSWORD = '' # password
MONGO_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_STORAGE_SERVER_READ = 'secondaryPreferred'
```

# Result_storages

## mongodb_webp_result_storage

Description: Mise en cache des images pour MongoDB compatible avec la fonction auto_webp.

Implementation: 
```
STORAGE = thumbor_ftvnum_libs.result_storages.mongo_webp_result_storage
```

Options:
```
MONGO_RESULT_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_RESULT_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_RESULT_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_RESULT_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_RESULT_STORAGE_SERVER_USER = '' # user
MONGO_RESULT_STORAGE_SERVER_PASSWORD = '' # password
MONGO_RESULT_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_RESULT_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_RESULT_STORAGE_SERVER_READ = 'secondaryPreferred'
```

Note: avec utilisation de Varnish quelques modifs sont réaliser

Exemple: https://www.fastly.com/blog/test-new-encodings-fastly-including-webp

```
sub vcl_recv {
  # Normalize Accept, we're only interested in webp right now.
  # And only normalize for URLs we care about.
  if (req.http.Accept && req.url ~ "(\.jpe?g|\.png)($|\?)") {
    # So we don't have to keep using the above regex multiple times.
    set req.http.X-Is-An-Image-URL = "yay";

    # Test Le wep n'est pas acceptable
    if (req.http.Accept ~ "image/webp[^,];q=0(\.0?0?0?)?[^0-9]($|[,;])") {
      unset req.http.Accept;
    }

    # Le webp est acceptable
    if (req.http.Accept ~ "image/webp") {
      set req.http.Accept = "image/webp";
    } else {
      # Header non present
      unset req.http.Accept;
    }
  }
#FASTLY recv
}

sub vcl_miss {
  # Si vous avez /foo/bar.jpeg, vous pouvez aussi avoir /foo/bar.webp

  if (req.http.Accept ~ "image/webp" && req.http.X-Is-An-Image-URL) {
    set bereq.url = regsuball(bereq.url, "(\.jpe?g|\.png)($|\?)", ".webp\2");
  }
#FASTLY miss
}

sub vcl_fetch {
  if (req.http.X-Is-An-Image-URL) {
    if (!beresp.http.Vary ~ "(^|\s|,)Accept($|\s|,)") {
      if (beresp.http.Vary) {
        set beresp.http.Vary = beresp.http.Vary ", Accept";
      } else {
         set beresp.http.Vary = "Accept";
      }
    }
  }
#FASTLY fetch
}
```

## mongodb_result_storage

Description: Mise en cache des images pour MongoDB (Legacy).

Implementation: 
```
STORAGE = thumbor_ftvnum_libs.result_storages.mongo_result_storage
```

Options:
```
MONGO_RESULT_STORAGE_SERVER_HOST = 'localhost' # MongoDB storage server host
MONGO_RESULT_STORAGE_SERVER_PORT = 27017 # MongoDB storage server port
MONGO_RESULT_STORAGE_SERVER_DB = 'thumbor' # MongoDB storage server database name
MONGO_RESULT_STORAGE_SERVER_COLLECTION = 'images' # MongoDB storage image collection
MONGO_RESULT_STORAGE_SERVER_USER = '' # user
MONGO_RESULT_STORAGE_SERVER_PASSWORD = '' # password
MONGO_RESULT_STORAGE_SERVER_AUTH = '' # credential stored in this db
MONGO_RESULT_STORAGE_SERVER_REPLICASET = 'myReplica' # name of the replicaset - option
MONGO_RESULT_STORAGE_SERVER_READ = 'secondaryPreferred'
```