#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Greg Reda'
SITENAME = u'Greg Reda'
SITEURL = 'http://www.gregreda.com'
TIMEZONE = 'America/Los_Angeles'
DESCRIPTION = u"Greg Reda is a software engineer and data scientist based in San Francisco"
INDEX_PAGE_HEADER = 'Nice to meet you.'

# Variables for theme
THEME = 'newbird/'
LOGO_IMAGE = '/images/logo.jpg'
FAVICON_IMAGE = '/images/favicon.ico'
COPYRIGHT_START_YEAR = 2013
NAV_LINKS = [
    {'name': 'Home', 'url': '/'},
    {'name': 'Blog', 'url': '/blog/'},
    {'name': 'Talks', 'url': '/talks/'},
    {'name': 'About', 'url': '/about/'},
]

# URL paths
AUTHOR_SAVE_AS = ''  # I'm the only author
AUTHORS_SAVE_AS = ''

ARTICLE_PATHS = ['blog']
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'


# DEFAULTS
USE_FOLDER_AS_CATEGORY = False
DEFAULT_LANG = 'en'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PAGINATION = False

# FEEDS
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/category/%s.atom.xml"
TAG_FEED_ATOM = "feeds/tag/%s.atom.xml"

MARKUP = ('md', 'ipynb')

# Plugins
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['pelican-ipynb.liquid', 'sitemap']

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'monthly',
        'pages': 'monthly'
    }
}

CODE_DIR = 'code'
NOTEBOOK_DIR = 'notebooks'

STATIC_PATHS = ['images', 'code', 'notebooks', 'extra', 'data']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

#### Analytics
GOOGLE_ANALYTICS = 'UA-34295039-1'
DOMAIN = "gregreda.com"

# Other
CACHE_CONTENT = False
AUTORELOAD_IGNORE_CACHE = True

# Social Sharing
TWITTER_CARDS = True
TWITTER_NAME = "gjreda"