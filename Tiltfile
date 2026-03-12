load('ext://namespace', 'namespace_create', 'namespace_inject')
load('ext://secret', 'secret_create_generic')

# 1. Local Setup Automation
# Synchronously ensure .env exists so Tilt can mount it as a K8s secret
if str(local("test -f .env && echo 'exists' || echo 'missing'", quiet=True)).strip() == 'missing':
    local("cp .env.example .env", quiet=True)

# Synchronously ensure the guardrail key exists in .env
if str(local('grep -q "^LLM_GUARDRAIL_SECRET_KEY=" .env && echo "exists" || echo "missing"', quiet=True)).strip() == 'missing':
    local("make generate-guardrail-key", quiet=True)

local_resource(
  'install-deps',
  cmd='uv sync',
  deps=['pyproject.toml', 'uv.lock'],
  labels=['setup']
)

# Allow manual regeneration of the guardrail key from the UI
local_resource(
    'regenerate-guardrail-key',
    cmd='make generate-guardrail-key',
    labels=['setup'],
    trigger_mode=TRIGGER_MODE_MANUAL
)

# Ensure the required local guardrail model is pulled in Ollama
local_resource(
    'ollama-model',
    cmd='ollama list | grep -q "llama3.1:8b" || ollama pull llama3.1:8b',
    labels=['setup']
)

# 2. Build Image
docker_build('bestow-poc-app', '.', dockerfile='Dockerfile')

# 3. Infrastructure setup (Namespace & Secret)
setup_objects = ['bestow-poc:namespace']
namespace_create('bestow-poc')

secret_create_generic('bestow-env', namespace='bestow-poc', from_env_file='.env')
setup_objects.append('bestow-env:secret')

# Allow manual force-update of the K8s secret if developers add keys to .env later
local_resource(
    'overwrite-k8s-secret',
    cmd='kubectl create secret generic bestow-env --namespace bestow-poc --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -',
    labels=['infra'],
    trigger_mode=TRIGGER_MODE_MANUAL
)

# This call groups the namespace and secret into one UI resource
k8s_resource(
    new_name='cluster-setup',
    objects=setup_objects,
    labels=['infra']
)

# 4. Deploy YAMLs
k8s_yaml(namespace_inject(read_file('deploy/local/k8s/api.yaml'), 'bestow-poc'))
k8s_yaml(namespace_inject(read_file('deploy/local/k8s/ui.yaml'), 'bestow-poc'))
# k8s_yaml(namespace_inject(read_file('deploy/local/k8s/ollama.yaml'), 'bestow-poc'))

# 5. Resource definitions
k8s_resource('api', port_forwards=['8000:8000', '5678:5678'], labels=['apps'])
k8s_resource('ui', port_forwards=['8501:8501', '5679:5679'], labels=['apps'])
# k8s_resource('ollama', port_forwards=['11434:11434'], labels=['apps'])
