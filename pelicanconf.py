#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Greg Reda'
SITENAME = u'Greg Reda'
SITEURL = 'http://www.gregreda.com'
TIMEZONE = 'America/Chicago'
TITLE = u"Greg Reda"
DESCRIPTION = u"Greg Reda is a data scientist based in San Francisco"

# Variables for theme
THEME = 'void/'
LOGO_IMAGE = '/images/logo.jpg'
COPYRIGHT_START_YEAR = 2013
NAVIGATION = [
    {'site': 'twitter', 'user': 'gjreda', 'url': 'https://twitter.com/gjreda'},
    {'site': 'github', 'user': 'gjreda', 'url': 'https://github.com/gjreda'},
    {'site': 'linkedin', 'user': 'gjreda', 'url': 'http://linkedin.com/in/gjreda'},
]

ARTICLE_URL = '{category}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'

# Static Pages
PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
ABOUT_PAGE_HEADER = 'Nice to meet you.'

# DEFAULTS
DEFAULT_LANG = 'en'
DEFAULT_CATEGORY = 'misc'
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%b %d, %Y'
DEFAULT_PAGINATION = False

# FEEDS
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/category/%s.atom.xml"
TAG_FEED_ATOM = "feeds/tag/%s.atom.xml"

MARKUP = ('md', 'ipynb')

# PLUGINS
PLUGIN_PATHS = ['pelican-plugins', 'pelican_dynamic']
PLUGINS = ['assets', 'pelican-ipynb.liquid', 'pelican_dynamic', 'sitemap']

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
# EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

STATIC_PATHS = ['images', 'code', 'notebooks', 'extra', 'data']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

TWITTER_CARDS = True
TWITTER_NAME = "gjreda"
FACEBOOK_SHARE = True
HACKER_NEWS_SHARE = True

#### Analytics
GOOGLE_ANALYTICS = 'UA-34295039-1'
DOMAIN = "gregreda.com"

# Other
CACHE_CONTENT = False
AUTORELOAD_IGNORE_CACHE = True
