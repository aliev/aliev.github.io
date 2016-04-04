from setuptools import setup

setup(
    name='lektor-markdown-tasks',
    version='0.1',
    author=u'Ali Aliev',
    author_email='shamkir@gmail.com',
    license='MIT',
    py_modules=['lektor_markdown_tasks'],
    entry_points={
        'lektor.plugins': [
            'markdown-tasks = lektor_markdown_tasks:MarkdownTasksPlugin',
        ]
    }
)
