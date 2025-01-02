from typing import Iterable
from unittest import TestCase
from ....framework import (
    RunConfiguration, TestReport, SmallImageBuilder, IImageBuilder, DockerWebServiceController,
    BrainBoxApi, BrainBoxTask, FileIO, INotebookableController, IModelDownloadingController, DownloadableModel
)
from .settings import BoilerplateSettings
from .model import BoilerplateModel
from pathlib import Path


class BoilerplateController(
    DockerWebServiceController[BoilerplateSettings],
    INotebookableController,
    IModelDownloadingController
):
    def get_image_builder(self) -> IImageBuilder|None:
        return SmallImageBuilder(
            Path(__file__).parent/'container',
            DOCKERFILE,
            DEPENDENCIES.split('\n'),
        )

    def get_downloadable_model_type(self) -> type[DownloadableModel]:
        return BoilerplateModel

    def get_service_run_configuration(self, parameter: str|None) -> RunConfiguration:
        if parameter is None:
            parameter = 'no_parameter'
        return RunConfiguration(
            parameter,
            publish_ports={self.connection_settings.port:8080},
            command_line_arguments=['--setting', self.settings.setting, '--parameter', parameter]
        )

    def get_notebook_configuration(self) -> RunConfiguration|None:
        return self.get_service_run_configuration('').as_notebook_service()

    def get_default_settings(self):
        return BoilerplateSettings()

    def create_api(self):
        from .api import Boilerplate
        return Boilerplate()

    def post_install(self):
        FileIO.write_text("Boilerplate resource", self.resource_folder()/'resource')
        FileIO.write_text("Boilerplate nested resource", self.resource_folder('nested') / 'resource')


    def _self_test_internal(self, api: BrainBoxApi, tc: TestCase) -> Iterable:
        from .api import Boilerplate

        api.execute(BrainBoxTask.call(Boilerplate, 'test_parameter').json('test_argument_json'))
        yield TestReport.last_call(api).with_comment("Returns JSON as a string. This string is stored in the database")

        api.execute(BrainBoxTask.call(Boilerplate, 'test_parameter').file('test_argument_file'))
        yield TestReport.last_call(api).result_is_file().with_comment("Returns a json as a file. It's content is not stored in the database, but in the file cache")

        api.execute(BrainBoxTask.call(Boilerplate, 'test_parameter').resources())
        yield TestReport.last_call(api).with_comment("Returns a json with the list of resources: files that are stored at the server outside of the cache, and are shared with the container")







DOCKERFILE = f'''
FROM python:3.11

{{{SmallImageBuilder.ADD_USER_PLACEHOLDER}}}

{{{SmallImageBuilder.PIP_INSTALL_PLACEHOLDER}}}

COPY . /home/app/

ENTRYPOINT ["python3","/home/app/main.py"]
'''

DEPENDENCIES = '''
anyio==4.7.0
argon2-cffi==23.1.0
argon2-cffi-bindings==21.2.0
arrow==1.3.0
asttokens==3.0.0
async-lru==2.0.4
attrs==24.3.0
babel==2.16.0
beautifulsoup4==4.12.3
bleach==6.2.0
blinker==1.9.0
certifi==2024.12.14
cffi==1.17.1
charset-normalizer==3.4.0
click==8.1.7
comm==0.2.2
debugpy==1.8.11
decorator==5.1.1
defusedxml==0.7.1
executing==2.1.0
fastjsonschema==2.21.1
Flask==3.1.0
fqdn==1.5.1
h11==0.14.0
httpcore==1.0.7
httpx==0.28.1
idna==3.10
ipykernel==6.29.5
ipython==8.31.0
isoduration==20.11.0
itsdangerous==2.2.0
jedi==0.19.2
Jinja2==3.1.4
json5==0.10.0
jsonpointer==3.0.0
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
jupyter-events==0.11.0
jupyter-lsp==2.2.5
jupyter_client==8.6.3
jupyter_core==5.7.2
jupyter_server==2.15.0
jupyter_server_terminals==0.5.3
jupyterlab==4.3.4
jupyterlab_pygments==0.3.0
jupyterlab_server==2.27.3
MarkupSafe==3.0.2
matplotlib-inline==0.1.7
mistune==3.0.2
nbclient==0.10.2
nbconvert==7.16.4
nbformat==5.10.4
nest-asyncio==1.6.0
notebook==7.3.1
notebook_shim==0.2.4
overrides==7.7.0
packaging==24.2
pandocfilters==1.5.1
parso==0.8.4
pexpect==4.9.0
platformdirs==4.3.6
prometheus_client==0.21.1
prompt_toolkit==3.0.48
psutil==6.1.1
ptyprocess==0.7.0
pure_eval==0.2.3
pycparser==2.22
Pygments==2.18.0
python-dateutil==2.9.0.post0
python-json-logger==3.2.1
PyYAML==6.0.2
pyzmq==26.2.0
referencing==0.35.1
requests==2.32.3
rfc3339-validator==0.1.4
rfc3986-validator==0.1.1
rpds-py==0.22.3
Send2Trash==1.8.3
six==1.17.0
sniffio==1.3.1
soupsieve==2.6
stack-data==0.6.3
terminado==0.18.1
tinycss2==1.4.0
tornado==6.4.2
traitlets==5.14.3
types-python-dateutil==2.9.0.20241206
typing_extensions==4.12.2
uri-template==1.3.0
urllib3==2.2.3
wcwidth==0.2.13
webcolors==24.11.1
webencodings==0.5.1
websocket-client==1.8.0
Werkzeug==3.1.3
'''

