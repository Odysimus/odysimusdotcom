# vim: set fileencoding=utf8 :
"""Some hooks that might be useful."""

import os
import subprocess
from StringIO import StringIO
import logging

from wok.exceptions import DependencyException
from wok.util import slugify

try:
    from lxml import etree
except ImportError:
    etree = None


class HeadingAnchors(object):
    """
    Put some paragraph heading anchors.

    Serves as a 'page.template.post' wok hook.
    """

    def __init__(self, max_heading=3):
        if not etree:
            raise DependencyException('To use the HeadingAnchors hook, you must '
                                      'install the library lxml.')
        self.max_heading = max_heading
        logging.debug('Loaded hook HeadingAnchors')

    def __call__(self, page):
        logging.debug('Called hook HeadingAnchors on {0}'.format(page))
        parser = etree.HTMLParser()
        sio_source = StringIO(page.rendered)
        tree = etree.parse(sio_source, parser)

        for lvl in range(1, self.max_heading+1):
            headings = tree.iterfind('//h{0}'.format(lvl))
            for heading in headings:
                if not heading.text:
                    continue
                logging.debug('[HeadingAnchors] {0} {1}'.format(heading, heading.text))

                name = 'heading-{0}'.format(slugify(heading.text))
                anchor = etree.Element('a')
                anchor.set('class', 'heading_anchor')
                anchor.set('href', '#' + name)
                anchor.set('title', 'Permalink to this section.')
                anchor.text = u'¶'
                heading.append(anchor)

                heading.set('id', name)

        sio_destination = StringIO()
        tree.write(sio_destination)
        page.rendered = sio_destination.getvalue()


def compile_sass(output_dir):
    '''
    Compile Sass files -> CSS in the output directory.

    Any .scss or .sass files found in the output directory will be compiled 
    to CSS using Sass. The compiled version of the file will be created in the 
    same directory as the Sass file with the same name and an extension of 
    .css. For example, foo.scss -> foo.css.

    Hook:

        site.output.post

    Dependencies:

        - Ruby
        - Sass (http://sass-lang.com)
    '''
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            fname, fext = os.path.splitext(f)
            if fext == ".scss" or fext == ".sass":
                abspath = os.path.abspath(root)
                sass_src = "%s/%s"%(abspath, f)
                sass_dest = "%s/%s.css"%(abspath, fname)
                sass_arg = "%s:%s"%(sass_src, sass_dest)
                subprocess.call(['sass', sass_arg])
