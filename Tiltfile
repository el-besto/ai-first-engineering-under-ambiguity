load('ext://namespace', 'namespace_create', 'namespace_inject')
load('ext://secret', 'secret_create_generic')

local_resource(
  'install-deps',
  cmd='uv sync',
  deps=['pyproject.toml', 'uv.lock']
)

docker_build('bestow-poc-app', '.', dockerfile='Dockerfile')

namespace_create('bestow-poc')

if str(local("test -f .env && echo 'exists' || echo 'missing'", quiet=True)).strip() == 'exists':
    secret_create_generic('bestow-env', namespace='bestow-poc', from_env_file='.env')

k8s_yaml(namespace_inject(read_file('deploy/local/k8s/api.yaml'), 'bestow-poc'))
k8s_yaml(namespace_inject(read_file('deploy/local/k8s/ui.yaml'), 'bestow-poc'))
k8s_yaml(namespace_inject(read_file('deploy/local/k8s/ollama.yaml'), 'bestow-poc'))

k8s_resource('api', port_forwards=['8000:8000', '5678:5678'])
k8s_resource('ui', port_forwards=['8501:8501'])
k8s_resource('ollama', port_forwards=['11434:11434'])
