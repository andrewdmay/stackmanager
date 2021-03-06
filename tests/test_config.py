import pytest
from stackmanager.config import Config


@pytest.fixture
def all_config():
    return Config({
        'Environment': 'all',
        'StackName': '{{ Environment }}-ExampleStack',
        'Template': 'template.yaml',
        'Parameters': {
            'Environment': '{{ Environment }}',
            'Thing': '/Company/{{ Environment }}/{{ Region }}/Thing',
            'This': 'That'
        },
        'Tags': {
            'Team': 'Ops',
            'TestFunction': '{{ Region|replace("us-", "u")|replace("east-","e")|replace("west-","w") }}'
        },
        'Capabilities': [
            'CAPABILITIES_IAM'
        ]
    })


@pytest.fixture
def dev_config(all_config):
    config = Config({
        'Environment': 'dev',
        'Region': 'us-east-1',
        'Parameters': {
            'This': 'TheOther',
            'Extra': '/Company/{{ Region }}/{{ Environment }}/Extra'
        },
        'Capabilities': [
            'CAPABILITIES_NAMED_IAM'
        ]
    })
    config.set_parent(all_config)
    return config


def test_is_all():
    assert Config.is_all('all')
    assert not Config.is_all('dev')


def test_environment(all_config, dev_config):
    assert all_config.environment == 'all'
    assert dev_config.environment == 'dev'


def test_region(all_config, dev_config):
    assert not all_config.region
    assert dev_config.region == 'us-east-1'


def test_stack_name(all_config, dev_config):
    assert all_config.stack_name == 'all-ExampleStack'
    assert dev_config.stack_name == 'dev-ExampleStack'


def test_template(all_config, dev_config):
    assert all_config.template == 'template.yaml'
    assert dev_config.template == 'template.yaml'


def test_capabilities(all_config, dev_config):
    assert all_config.capabilities == ['CAPABILITIES_IAM']
    assert dev_config.capabilities == ['CAPABILITIES_NAMED_IAM']


def test_parameters_all(all_config):
    assert all_config.parameters == {
        'Environment': 'all',
        'Thing': '/Company/all/None/Thing',
        'This': 'That'
    }


def test_parameters_dev(dev_config):
    assert dev_config.parameters == {
        'Environment': 'dev',
        'Thing': '/Company/dev/us-east-1/Thing',
        'This': 'TheOther',
        'Extra': '/Company/us-east-1/dev/Extra'
    }


def test_tags_all(all_config):
    assert all_config.tags == {
        'Team': 'Ops',
        'TestFunction': 'None'
    }


def test_tags_dev(dev_config):
    assert dev_config.tags == {
        'Team': 'Ops',
        'TestFunction': 'ue1'
    }


