from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='automated_therapy_system',
    version='1.0.0',
    author='Ashique J, Abishai S, Arun Ravisankkar',
    author_email='your.email@example.com',
    description='Automated Therapy System combining sound/music therapy and AI virtual therapist',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/automated-therapy-system',
    packages=find_packages(include=['therapy_app', 'therapy_app.*']),
    package_dir={'therapy_app': 'therapy_app'},
    include_package_data=True,
    install_requires=[
        'python-vlc>=3.0.12',
        'tensorflow>=2.10.0',
        'nltk>=3.8.1',
        'mutagen>=1.46.0',
        'ttkthemes>=3.2.2',
        'numpy>=1.24.3',
        'pillow>=10.0.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.8',
    entry_points={
        'gui_scripts': [
            'automated-therapy=therapy_app.main:main'
        ]
    },
    data_files=[
        ('data', ['data/intents.json']),
        ('models', ['models/words.pkl', 'models/classes.pkl', 'models/therapist_model.h5'])
    ],
    keywords='therapy mental-health ai sound-processing',
    project_urls={
        'Source': 'https://github.com/yourusername/automated-therapy-system',
        'Documentation': 'https://github.com/yourusername/automated-therapy-system/docs'
    }
)
