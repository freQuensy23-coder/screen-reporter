from setuptools import setup

APP = ['daemon.py']
DATA_FILES = [
    'prompt.md',
    'costs.json',
    '.env'
]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'LSBackgroundOnly': True,
    },
    'packages': [
        'openai',
        'PIL',
        'tqdm',
        'python-dotenv',
        'loguru'
    ],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
) 