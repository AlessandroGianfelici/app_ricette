from setuptools import setup, find_packages

setup(name='resipes',
      version='0.1.0',
      description='Utility for recipe data',
      url='https://github.com/AlessandroGianfelici/app_ricette',
      author='Alessandro Gianfelici',
      author_email='alessandro.gianfelici@hotmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
            'recipe-scrapers',
            'parse-ingredients',
            'pandas',
            'pyarrow '
      ],
      zip_safe=False)
