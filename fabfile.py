from fabric.api import lcd, local

def push():
    local('git co master')
    local('git merge --no-ff dev')
    local('git push --all origin')
    local('git co dev')

def deploy_staging():
    with lcd('../staging/'):
        local('git st')
        local('git pull origin master')
        local('sudo supervisorctl restart qdb-staging')

def deploy_production():
    with lcd('../production/'):
        local('git pull origin master')
        local('python manage.py migrate qdbapp')
        local('sudo supervisorctl restart qdb-production')
