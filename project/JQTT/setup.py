from setuptools import setup

# Function to open the README file.
def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='JQTT',
      version='0.1',
      description='Simplified MQTT library',
	  long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
		'Environment :: Console',
        'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Communications',
		'Topic :: Utilities'
      ],
	  keywords='MQTT pub sub broker client',
      url='http://github.com/jaimeloeuf',
      author='Jaime Loeuf',
      author_email='jaimeloeuf@gmail.com',
      license='MIT',
      packages=['JQTT'],
	  install_requires=['paho-mqtt'],
	  include_package_data=True,
      zip_safe=False)