# Configuration

This folder exists for all your configuration, both KernelAI related and
separate.

## Local configuration

Local configuration contains configuration that is either
user-specific (e.g. IDE configuration) or protected (e.g. security keys).

WARNING: Please do not check in local configuration to version control.

You can use this readme to provide instructions for reproducing local
configuration.

## Base configuration

Base configuration is where all shared configuration is stored. This is
applicable for any non-sensitive and project-related configuration that should
be shared across team members.

WARNING: Please do not put access credentials in base configuration.

## KernelAI configuration

KernelAI-specific configuration (e.g., DataCatalog configuration for IO)
will merge base and local configuration at runtime.

Whatever configuration is loaded with:

```python
from kernelai.config import ConfigLoader
conf_paths = ['conf/base', 'conf/local']
conf_loader = ConfigLoader(conf_paths)
conf = conf_loader.get('*some-glob-pattern*')
```

will contain the result of merging all the files matching patterns 
`conf/base/*some-glob-pattern*` and `conf/local/*some-glob-pattern*`, 
with local configuration taking priority.

This can be used for testing purposes without affecting what will be committed 
to version control.
