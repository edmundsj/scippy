import sys
import os
import fileinput

root_dir = os.getcwd()
old_name = 'tabularasa'
module_name = root_dir.split('/')[-1]


print(f' Detected module name {module_name}. Is this correct (y/n) ?')
yes_no = input()

if yes_no == 'y':
    print(f'Please provide a brief description of your package:\n')
    description = input()
    os.system('git config core.hooksPath .hooks')
    os.system(f'git remote set-url origin https://github.com/edmundsj/{module_name}.git')
    os.rename(old_name, module_name)

    files_to_read = [
        '.github/workflows/python-package-conda.yml',
        '.hooks/pre-commit',
        './' + module_name + '/__init__.py',
        'setup.py',
        './docs/source/conf.py',
        './' + module_name + '/test/test_something.py'
    ]

    for filename in files_to_read:
        with fileinput.FileInput(
                filename, inplace=True) as fh:
            for line in fh:
                print(line.replace(old_name, module_name), end='')

    with fileinput.FileInput('setup.py', inplace=True) as fh:
        for line in fh:
            print(line.replace('ADD SHORT DESCRIPTION HERE', description), end='')

    print('Adding all files to github ...')
    os.system('git add -A')
    os.system(f'git commit -m "Script auto-setting up repository for first use with name {module_name}..."')
    os.system('git push')
    print('Adding and switching to develop branch...')
    os.system('git branch develop')
    os.system('git checkout develop develop')
    os.system('git push --set-upstream origin develop')
