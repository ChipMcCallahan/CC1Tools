from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='cc1_tools',
    url='https://github.com/ChipMcCallahan/CC1Tools',
    author='Chip McCallahan',
    author_email='thisischipmccallahan@gmail.com',
    # Needed to actually package something
    packages=['cc1_tools'],
    package_dir={'cc1_tools': 'src'},
    # Needed for dependencies
    install_requires=['protobuf'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='LICENSE',
    description='Assorted tools for working with and displaying Chip\'s Challenge levels in DAT file format.',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)