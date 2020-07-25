#!/usr/bin/env python3

import os
from lettersmith import *
import config

environment = os.getenv('BUILD_ENV', 'development')
build_config = config.deploy if environment == 'deploy' else config.development

base_url = build_config.base_url
site_title = 'My notes'

static = files.find('static/**/*')

pages = pipe(
    docs.find('**/*.md'),
    docs.remove_index,
    docs.remove_drafts,
    permalink.rel_page_permalink('.'),
    docs.uplift_frontmatter,
    docs.with_template('page.html'),
)

home = pipe(
    docs.find('index.md'),
    permalink.rel_page_permalink('.'),
    docs.uplift_frontmatter,
    docs.with_template('index.html'),
)

all_pages = pipe(
    (*pages, *home),
    wikidoc.content_markdown(base_url),
    absolutize.absolutize(base_url),
)

context = {
    'site': {
        'title': site_title,
    },
    'base_url': base_url
}

rendered_docs = pipe(
    (all_pages),
    jinjatools.jinja('templates', base_url, context)
)

write(chain(static, rendered_docs), directory='public')

print('Done!')
