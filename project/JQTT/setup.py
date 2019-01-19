from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='funniest',
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
	  keywords='MQTT',
      url='http://github.com/storborg/funniest',
      author='Jaime Loeuf',
      author_email='jaimeloeuf@gmail.com',
      license='MIT',
      packages=['funniest'],
	  install_requires=[
          'paho.mqtt.publish',
      ],
	  include_package_data=True,
      zip_safe=False)