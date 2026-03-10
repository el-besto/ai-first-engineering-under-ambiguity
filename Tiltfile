local_resource(
  'install-deps',
  cmd='uv sync',
  deps=['pyproject.toml', 'uv.lock']
)

docker_build('bestow-poc-app', '.', dockerfile='Dockerfile')

k8s_yaml('deploy/local/k8s.yaml')

k8s_resource('api', port_forwards=['8000:8000'])
k8s_resource('ui', port_forwards=['8501:8501'])
