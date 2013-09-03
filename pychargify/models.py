"""
Chargify base models
"""
import six
import json
import requests
import dateutil.parser

from pychargify import get_version, exceptions


def headers():
    """
    Headers to send on every request
    """
    return {
        'user-agent': "pyChargify/{0}".format(get_version()),
        'content-type': 'application/json'
    }


def check_response_code(status_code):
    """
    Helper method to check response code errors after
    API calls.
    """
    # Unauthorized Error
    if status_code == 401:
        raise exceptions.ChargifyUnAuthorized()

    # Forbidden Error
    elif status_code == 403:
        raise exceptions.ChargifyForbidden()

    # Not Found Error
    elif status_code == 404:
        raise exceptions.ChargifyNotFound()

    # Unprocessable Entity Error
    elif status_code == 422:
        raise exceptions.ChargifyUnProcessableEntity()

    # Generic Server Errors
    elif status_code in [405, 500]:
        raise exceptions.ChargifyServerError()


class ChargifyField(object):
    """
    Base Field used in model
    """
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return self.value

    def to_python(self):
        """
        Create a python representation of the value.

        Override this to handle different data types.
        """
        return self.value or u''

    def to_string(self):
        """
        Return the python representation to a string.
        """
        return self.value or ''


class ChargifyDateField(ChargifyField):
    """
    Converts Date strings from chargify into python datetime objects.
    """
    def to_python(self):
        if isinstance(self.value, six.text_type):
            return dateutil.parser.parse(self.value) if self.value else None
        return self.value

    def to_string(self):
        return '' if not self.value else self.to_python().isoformat()


#pylint: disable=R0903
class MetaClass(object):
    """
    Meta options class used when instantiating a model
    """
    def __init__(self, meta_cls, **kwargs):  # pylint: disable=W0142
        self.url = kwargs.pop('url')
        self.key = kwargs.pop('key')
        self.fields = kwargs.pop('fields')
        self.field_cache = {}
        self.raw_content = None

        for item in dir(meta_cls):
            if item not in ('__doc__', '__module__', '__weakref__'):
                if not getattr(self, item, None):
                    setattr(self, item, getattr(meta_cls, item))


class ModelBase(type):
    """
    Borrowed liberally from Django

    https://github.com/django/django/blob/master/django/db/models/base.py
    """
    def __new__(cls, name, bases, attrs):
        super_cls = super(ModelBase, cls).__new__

        if name == 'NewBase' and attrs == {}:
            return super_cls(cls, name, bases, attrs)

        parents = [b for b in bases if isinstance(b, ModelBase) and
            not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))]

        if not parents:
            return super_cls(cls, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_cls(cls, name, bases, {'__module__': module})

        meta_attr = attrs.pop('Meta', None)

        meta_kwargs = {
            'url': getattr(meta_attr, 'url', None),
            'key': getattr(meta_attr, 'key', None),
            'fields': []
        }

        for obj_name, obj in attrs.items():
            setattr(new_class, obj_name, obj)

            if isinstance(obj, ChargifyField):
                meta_kwargs['fields'].append(obj_name)

        setattr(new_class, '_meta', MetaClass(meta_attr, **meta_kwargs))
        return new_class


class Model(six.with_metaclass(ModelBase)):
    """
    Model
    """
    api_key = ''
    sub_domain = ''
    base_host = '.chargify.com'
    request_host = ''

    def __init__(self, apikey, subdomain):
        """
        Initialize the Class with the API Key and SubDomain for Requests
        to the Chargify API
        """
        self.api_key = apikey
        self.sub_domain = subdomain
        self.request_host = "https://{0}{1}".format(
            self.sub_domain,
            self.base_host
        )

        fields = iter(self._meta.fields)
        field_cache = self._meta.field_cache = {}

        for field in fields:
            field_cache.update({
                field: getattr(self, field)
            })
            val = getattr(self, field).to_python()
            setattr(self, field, val)

    def __setattr__(self, key, value):
        if key in self._meta.field_cache:
            field = self._meta.field_cache.get(key)
            field.value = value

        super(Model, self).__setattr__(key, value)

    def __repr__(self):
        return '<{0}: {1}>'.format(self.__class__.__name__, self.__unicode__())

    def __str__(self):
        return '{0} object'.format(self.__class__.__name__)

    # pylint: disable=R0201
    def __unicode__(self):
        return u''

    def setup_url(self, obj_id=None):
        """
        Automatically change the URL set on the inner meta class when an ID
        is set.
        """
        url = getattr(self._meta, 'url', None)
        if not url:
            raise exceptions.ChargifyError(
                'A URL is required in the model Meta class')

        if obj_id:
            url_parts = url.split('.json')
            return '{0}/{1}.json'.format(url_parts[0], obj_id)

        return url

    def process_result(self, content):
        """
        Turn the raw JSON into model classes
        """
        if isinstance(content, list):
            out = []
            for obj in content:
                out.append(self.parse(obj.get(self._meta.key)))
            return out
        elif isinstance(content, dict):
            # single row
            return self.parse(content.get(self._meta.key))
        else:
            return []

    def get(self, object_id=None):
        """
        Performs an HTTP GET request.

        If an ``object_id`` keyword argument is present, the URL will be
        automatically changed to GET the specific ID.
        """
        url = self.setup_url(obj_id=object_id)
        content = self._get(url)
        return self.process_result(content)

    def save(self):
        """
        "Save" this object by performing an API call.

        If the ``id`` attr is on the object, alter the URL.
        """
        # pylint: disable=E1101
        if hasattr(self, 'id') and isinstance(self.id, int):
            url = self.setup_url(obj_id=self.id)
        else:
            url = self.setup_url()

        obj = self._save(url, self._meta.key)
        return self.parse(obj.get(self._meta.key), create_new_class=False)

    def _get(self, url):
        """
        Handle HTTP GET's to the API
        """
        response = requests.get(
            "{0}/{1}".format(self.request_host, url.lstrip('/')),
            auth=(self.api_key, 'x'),
            headers=headers())

        check_response_code(response.status_code)

        return response.json()

    def _post(self, url, payload):
        """
        Handle HTTP POST's to the API
        """
        response = requests.post(
            "{0}/{1}".format(self.request_host, url.lstrip('/')),
            auth=(self.api_key, 'x'),
            headers=headers(),
            data=json.dumps(payload)
        )

        check_response_code(response.status_code)
        return response.json()

    def _put(self, url, payload):
        """
        Handle HTTP PUT's to the API
        """
        response = requests.put(
            "{0}/{1}".format(self.request_host, url.lstrip('/')),
            auth=(self.api_key, 'x'),
            headers=headers(),
            data=json.dumps(payload)
        )

        check_response_code(response.status_code)
        return response.json()

    # def _delete(self, url, data):
    #     """
    #     Handle HTTP DELETE's to the API
    #     """
    #     return self._request('DELETE', url, data)

    def _save(self, url, node_name):
        """
        Save the object using the passed URL as the API end point
        """
        obj_dict = {}

        for item in self._meta.fields:
            if item not in self._meta.read_only_fields:
                obj_dict.update({
                    item: self._meta.field_cache.get(item).to_string()
                })

        payload = {node_name: obj_dict}

        # pylint: disable=E1101
        if self.id:
            return self._put(url, payload)

        return self._post(url, payload)

    def _set_val(self, name, value):
        """
        Set the value on the class object as well as the Meta field cache
        object.
        """
        cls_field = self._meta.field_cache.get(name)
        cls_field.value = value

        field = getattr(self, name)
        field = cls_field.to_python()
        return field

    def parse(self, content, create_new_class=True):
        """
        Parse the content of the API call.
        """
        if create_new_class:
            klass = self.__class__(self.api_key, self.sub_domain)
        else:
            klass = self
        self._meta.raw_content = content
        for row in content:
            if self._meta.field_cache.get(row):
                if hasattr(self._meta, 'attribute_types'):
                    if row in self._meta.attribute_types.keys():
                        from pychargify import api
                        field_class_name = self._meta.attribute_types.get(row)
                        field_class = getattr(api, field_class_name)(
                            self.api_key, self.sub_domain)

                        field_class.parse(content.get(row))
                        setattr(klass, row, field_class)
                    else:
                        setattr(klass,
                                row, self._set_val(row, content.get(row)))
                else:
                    setattr(klass, row, self._set_val(row, content.get(row)))

        return klass
