import pytest

from datadog_checks.base import ConfigurationError
from datadog_checks.controlplane import ControlplaneCheck


@pytest.mark.unit
def test_config():
    instance = {}
    c = ControlplaneCheck('controlplane', {}, [instance])

    # empty instance
    with pytest.raises(ConfigurationError):
        c.check(instance)

    # only the url
    with pytest.raises(ConfigurationError):
        c.check({'url': 'http://foobar'})

    # only the search string
    with pytest.raises(ConfigurationError):
        c.check({'search_string': 'foo'})

    # this should not fail
    c.check({'url': 'http://foobar', 'search_string': 'foo'})


@pytest.mark.integration
@pytest.mark.usefixtures('dd_environment')
def test_service_check(aggregator, instance):
    c = ControlplaneCheck('controlplane', {}, [instance])

    # the check should send OK
    c.check(instance)
    aggregator.assert_service_check('controlplane.search', ControlplaneCheck.OK)

    # the check should send WARNING
    instance['search_string'] = 'Apache'
    c.check(instance)
    aggregator.assert_service_check('controlplane.search', ControlplaneCheck.WARNING)
