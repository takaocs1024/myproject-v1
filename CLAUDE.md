# CLAUDE.md

Django を使った Web アプリケーション開発の学習プロジェクト。

## 技術スタック

| 技術 | バージョン | 用途 |
| ----- | ----- | -----|
| Ubuntu | 24.04 | 開発環境。UTM で構築。|
| Python | 3.14.3 | メインプログラミング言語 |
| Django | 6.0.4 | メインフレームワーク|
| SQLite3 | 3 | 開発用データベース|

## ディレクトリ構造

```
myproject/
    apps/               # アプリディレクトリはここにまとめる。
        __init__.py
    config/
        __init__.py
        asgi.py
        settings.py
        test.py
        urls.py
        wsgi.py
    requirements/
        base.txt
        local.txt
    static/
    templates/
```

## 開発コマンド

- マイグレーションファイル作成: `python manage.py makemigrations`
- マイグレーション: `python manage.py migrate`
- 起動コマンド: `python manager.py runserver 192.168.64.7:8000`
- テストコマンド: `python manage.py test --settings=config.test`
- コードチェック: `flake8`

## ルール

- Python コマンドは `python` を使用すること。`python3` や `pyenv exec python` で実行しないこと。
- テストコマンド実行には、必ず `--settings=config.test` を付けて実行すること。なお、テストコマンド実行以外では `--settings=confing.test` は付けないこと。 
- `apps` ディレクトリにアプリディレクトリをまとめるため、`startapp` コマンドは `apps` ディレクトリ内で実行すること。