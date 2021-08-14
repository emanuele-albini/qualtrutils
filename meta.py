from configparser import ConfigParser
from jinja2 import Template, StrictUndefined

TEMPLATE_FILE = 'meta.jinja.yaml'
DEST_FILE = 'meta.yaml'
CFG_FILE = 'setup.cfg'

# Load template
with open(TEMPLATE_FILE, 'r') as f:
    meta = f.read()

with open(CFG_FILE, 'r') as f:
    cfg = f.read()


class RecoursiveParser(ConfigParser):
    def get_dict(self, section, option, key):
        parser_ = ConfigParser()
        parser_.read_string(f'[{option}]\n' + self.get(section, option))
        return parser_.get(option, key)

    def get_list(self, section, option):
        return [s.strip() for s in self.get(section, option).strip().split('\n')]


parser = RecoursiveParser()
parser.read_string(cfg)

meta = Template(meta, undefined=StrictUndefined).render(
    name=parser.get('metadata', 'name'),
    version=parser.get('metadata', 'version'),
    home=parser.get('metadata', 'url'),
    description=parser.get('metadata', 'description'),
    doc_url=parser.get_dict('metadata', 'project_urls', 'Documentation'),
    dev_url=parser.get_dict('metadata', 'project_urls', 'Source Code'),
    install_requires=parser.get_list('options', 'install_requires'),
)

# Save configuration
with open(DEST_FILE, 'w') as f:
    f.write(meta)