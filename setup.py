from setuptools import setup

setup(name='cldx',
      version='0.1',
      description='Causal Loop Diagrams with networkx',
      url='http://github.com/fabid/cldx',
      author='Fabian Dubois',
      author_email='fabian.dubois@gmail.com',
      license='MIT',
      packages=['cldx'],
      install_requires=[
            'matplotlib == 2.2.2',
            'numpy >=1.7.1',
            'networkx >= 2.1',
            'pygraphviz >= 1.3.1',
      ],
      zip_safe=False)
