local_resource(
  'install-deps',
  cmd='uv sync',
  deps=['pyproject.toml', 'uv.lock']
)

docker_build('bestow-poc-app', '.', dockerfile='Dockerfile')

k8s_yaml(
  local('docker compose -f deploy/local/compose.yaml config')
)

k8s_resource('app', port_forwards=['8000:8000'])
