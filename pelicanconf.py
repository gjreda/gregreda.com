#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Greg Reda'
SITENAME = u'Greg Reda'
EMAIL_ADDRESS = u'gjreda@gmail.com'
SITEURL = 'http://www.gregreda.com'
TIMEZONE = 'America/Chicago'
THEME = 'void/'
AVATAR = '/theme/images/avatar.jpg'
TITLE = "Greg Reda: Data scientist in Chicago."
DESCRIPTION = "Greg Reda is a Chicagoan focused on analyzing data to provide\
 insight and drive decisions. He loves stats, startups, sports, beer, and music."

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
PLUGIN_PATHS = ['../pelican-plugins',]
PLUGINS = ['assets', 'liquid_tags.notebook', 'pelican_dynamic', 'render_math']

CODE_DIR = 'code'
NOTEBOOK_DIR = 'notebooks'
EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

STATIC_PATHS = ['images', 'code', 'notebooks', 'extra']
EXTRA_PATH_METADATA = {'extra/robots.txt': {'path': 'robots.txt'},}

# NAVBAR
NAVIGATION = [
    (),
]

# SOCIAL
TWITTER_CARDS = True
TWITTER_NAME = "gjreda"
GITHUB_NAME = 'gjreda'
LINKEDIN_URL = 'http://linkedin.com/in/gjreda'
GOOGLE_PLUS_URL = 'https://plus.google.com/111658599948853828157?rel=author'
LASTFM_NAME = 'gjreda'
# DISQUS_SITENAME = 'gregreda'
# GITTIP_NAME = 'gjreda'

#### Analytics
GOOGLE_ANALYTICS = 'UA-34295039-1'
GOOGLE_ADSENSE = False
DOMAIN = "gregreda.com"

# Other
MAILCHIMP = True
CACHE_CONTENT = False
AUTORELOAD_IGNORE_CACHE = True
