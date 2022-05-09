import io
import urllib.request
import logging

import six
from ckan.plugins import toolkit
from ckan import model

from ckanext.datasetversions.helpers import TemporaryFileStorage


log = logging.getLogger(__name__)


def transfer_resource(resource, package_id, user, queue='default'):
    context_ = {'model': model, 'user': user, 'session': model.Session}
    url = resource.pop('url')
    log.info(f"Downloading resource form {url}")
    # Download the file from `url` and save it locally under `tmp_file`:
    try:
        response = urllib.request.urlopen(url)
    except Exception as e:
        log.exception(e)
    log.info(f"Successfully downloaded resource form {url}", )

    filename = url.rsplit('/', 1)[-1]
    data = six.ensure_binary(response.read())
    buffer = io.BytesIO(data)
    out_file = TemporaryFileStorage(buffer, filename)

    resource.pop('id')
    # # Change the "id" to the "id" of the "new datset"
    resource.pop('package_id')
    resource['package_id'] = package_id

    resource['upload'] = out_file

    try:
        toolkit.get_action('resource_create')(context_, resource)
    except Exception as e:
        log.exception(e)
    log.info("Successfully transfered {res_name}".format(
        res_name=resource['name']))
