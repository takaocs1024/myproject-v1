---
name: django-startproject
description: Django プロジェクトの初期設定を行う。
---

## 手順 1: プロジェクト作成

以下のコマンドを実行する。  
ただし、**すでに config ディレクトリがある場合は実行しないこと**。

```bash
django-admin startproject config .
```

## 手順 2: .env ファイルの作成

`.env` ファイルを作成する。作成する場所はルートディレクトリ直下とする。  
**既に存在する場合は作成する必要はない**。

```bash
touch .env
```

以降の作業で適宜 `.env` ファイルに環境変数を設定すること。

## 手順 3: config/settings.py の編集

生成された `config/settings.py` を読み込み、以下のルールに従って編集する。

### 共通ルール

- ファイル先頭に `# -*- coding: utf-8 -*-` を追加し、その直後に空白行を 1 行追加する。
- デフォルトで記述されているコメントは消さないこと。

### 環境変数の管理（django-environ）

`import environ` は `from pathlib import Path` の上に追記する。

```python
import environ
from pathlib import Path
```

`env = environ.Env()` 以降は `BASE_DIR = Path(__file__).resolve().parent.parent` の直後に追記する。

```python
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
READ_ENV_FILE = env.bool('DJANGO_READ_ENV_FILE', default=True)
if READ_ENV_FILE:
    env.read_env(BASE_DIR / '.env')

# 環境の種類。独自の変数。
ENVIRONMENT = env('DJANGO_ENVIRONMENT')
```

`DJANGO_ENVIRONMENT` は `local` を `.env` ファイルに設定すること。

### SECRET_KEY

既存の `SECRET_KEY = ...` 行を以下に置き換える。

```python
SECRET_KEY = env('DJANGO_SECRET_KEY')
```

`DJANGO_SECRET_KEY` を `.env` ファイルに設定すること。

### DEBUG

既存の `DEBUG = ...` 行を以下に置き換える。

```python
DEBUG = env.bool('DJANGO_DEBUG', default=False)
```

`DJANGO_DEBUG` はローカル開発環境のため `true` を `.env` ファイルに設定すること。

### ALLOWED_HOSTS

既存の `ALLOWED_HOSTS = ...` 行を以下に置き換える。

```python
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')
```

`DJANGO_ALLOWED_HOSTS` を `.env` ファイルに設定すること。

### INSTALLED_APPS

`django.contrib.staticfiles` の直後に以下を追加する。

```python
    # 便利なテンプレートタグの追加。
    'django.contrib.humanize',
    # Apps
    # Third Party
```

### TEMPLATES

`DIRS` を以下に変更する。

```python
'DIRS': [
    BASE_DIR / 'templates'
],
```

`context_processors` に以下の 3 つを追加する（既存のエントリの後に追加）。

```python
                # 以下を追加。
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.tz',
```

### DATABASES

既存の `DATABASES = { ... }` ブロック全体を以下に置き換える。

```python
DATABASES = {
    'default': env.db('DATABASE_URL')
}
DATABASES['default']['OPTIONS'] = env.json('DATABASE_OPTIONS', default={})
```

ローカル開発環境のため、`DATABASE_URL` は `SQLite3` の設定をすること。  
なお、データベースファイルはルートディレクトリ直下とする。また、 `DATABASE_OPTIONS` は設定する必要はなし。

### 日本語設定

- `LANGUAGE_CODE = 'en-us'` を `LANGUAGE_CODE = 'ja'` に変更する。
- `TIME_ZONE = 'UTC'` を `TIME_ZONE = 'Asia/Tokyo'` に変更する。

### 静的ファイルの設定

`STATIC_URL` の後に以下を追加する。

```python
STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = env.path('DJANGO_STATIC_ROOT')
```

### セキュリティ設定

ファイル末尾に以下を追加する。直前の記述から空白行を 2 行追加すること。

```python


# SECURITY

# HTTP クッキーを有効にするための設定。
CSRF_COOKIE_HTTPONLY = env.bool('CSRF_COOKIE_HTTPONLY', default=True)
# XSS 対策。
SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER', default=True)
# このサイトを iframe で使用することを不可とする。
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS', default='DENY')

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)
# security.W006
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# security.W008
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
# security.W012
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
# security.W016
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
# security.W021
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=False)
```

ローカル開発環境なので、上記のセキュリティの値は `default` を使用する。そのため `.env` ファイルには設定する必要はない。

### セッション設定

セキュリティ設定の後に以下を追加する。直前の記述から空白行を 2 行追加すること。

```python


# SESSION

# ブラウザを閉じるとセッションは切れるようにする。
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# セッションの期間は 1 日。
SESSION_COOKIE_AGE = 86400
```

### カンマ区切り設定

セッション設定の後に以下を追加する。直前の記述から空白行を 2 行追加すること。

```python


# カンマ区切り設定。
NUMBER_GROUPING = 3
```

### Django Debug Toolbar

カンマ区切り設定の後に以下を追加する。直前の記述から空白行を 2 行追加すること。

```python


if ENVIRONMENT == 'local':
    # ローカル環境の場合、デバックツールバーを設定。
    INSTALLED_APPS += ['debug_toolbar']                                     # noqa
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']       # noqa
    INTERNAL_IPS = env.list('DJANGO_INTERNAL_IPS', default=['127.0.0.1'])
    # Docker 環境ではクライアント IP が 127.0.0.1 にならないため、
    # SHOW_TOOLBAR_CALLBACK で常に表示するように設定。
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }
```

## 手順 3: config/urls.py の編集

生成された `config/urls.py` を読み込み、以下のルールに従って編集する。

### 共通ルール

- ファイル先頭に `# -*- coding: utf-8 -*-` を追加し、その直後に空白行を 1 行追加する。
- デフォルトで記述されているコメントは消さないこと。

### include

`path` の前に `include` を追加する。

```python
from django.urls import include, path
```

### 静的ファイル・メディアファイルに必要なモジュールのインポート

静的ファイル・メディアファイルに必要なモジュールのインポートする。`from django.urls import include, path` の直後に空白行を 1 行追加して、記述する。
また、記述後は空白行を 2 行追加する。

```python

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


```

### Django 標準の管理画面のパスの変更

Django 標準の管理画面のパスを `dj/admin/` に変更する。

```python
urlpatterns = [
    # Django Admin
    path('dj/admin/', admin.site.urls),
]
```

### 静的ファイル・メディアファイルの追加

`urlpatterns` に静的ファイル・メディアファイルの設定を追加する。追加後は空白行を 2 行追加する。

```python
urlpatterns = [
    # Django Admin
    path('dj/admin/', admin.site.urls),
]
# Static Files
urlpatterns += staticfiles_urlpatterns()
# Media Files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


```

### Django Debug Toolbar の設定

`Django Debug Toolbar` の設定を追加する。

```python
# django-debug-toolbar
if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
```

## 手順 4: config/test.py の新規作成

`config/test.py` を新規作成し、以下の内容を書き込む。

```python
# -*- coding: utf-8 -*-

from .settings import *     # noqa


# 環境の種類。独自の変数。
ENVIRONMENT = 'test'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_PORT = 1025

STATIC_ROOT = None


# これを設定しないとテストできない。
DEBUG_TOOLBAR_CONFIG = {
    'IS_RUNNING_TESTS': False
}
```

## 完了後の確認

すべてのファイルを編集・作成し終えたら、変更内容を簡潔に報告する。
