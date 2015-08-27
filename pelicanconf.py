#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Greg Reda'
SITENAME = u'Greg Reda'
EMAIL_ADDRESS = u'gjreda@gmail.com'
SITEURL = 'http://www.gregreda.com'
TIMEZONE = 'America/Chicago'
THEME = 'void/'
AVATAR = '/theme/images/avatar.jpg'
TITLE = "Greg Reda: independent data science and strategy consulting."
DESCRIPTION = "Greg Reda is an independent data science and strategy \
consultant, helping clients effectively utilize data to gain insight, \
inform decisions, and grow their business."

# TODO: switch to /blog/slug/index.html -- need to setup redirects first
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'

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
TAG_FEED_ATOM = "feeds/tag/%s.atom.xml"

# PLUGINS
PLUGIN_PATHS = ['pelican-plugins', 'pelican_dynamic']
PLUGINS = ['assets', 'liquid_tags.notebook', 'pelican_dynamic', 'render_math']

CODE_DIR = 'code'
NOTEBOOK_DIR = 'notebooks'
EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

STATIC_PATHS = ['images', 'code', 'notebooks', 'extra', 'data']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

# TODO: NAVBAR - make it dynamic
NAVIGATION = [
    (),
]

# TODO: SOCIAL - make it dynamic
TWITTER_CARDS = True
TWITTER_NAME = "gjreda"
GITHUB_NAME = 'gjreda'
LINKEDIN_URL = 'http://linkedin.com/in/gjreda'
GOOGLE_PLUS_URL = 'https://plus.google.com/111658599948853828157?rel=author'
LASTFM_NAME = 'gjreda'

#### Analytics
GOOGLE_ANALYTICS = 'UA-34295039-1'
DOMAIN = "gregreda.com"

# Other
MAILCHIMP = True
CACHE_CONTENT = False
AUTORELOAD_IGNORE_CACHE = True
