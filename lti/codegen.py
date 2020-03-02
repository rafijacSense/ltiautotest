models = {
    'Context': {
    },
    'ResourceLink': {
    },
    'ToolPlatform': {
    },
    'LaunchPresentation': {
    },
    'Custom': {},
    'DeeplinkSettings': {
        'return_url': ["deep_link_return_url"],
        "accept_types": ['', 'List[str]'],
        "accept_media_types": ['', 'List[str]'],
        "accept_presentation_document_targets": ['', 'List[str]'],
        "accept_multiple": ['', 'bool'],
        "auto_create": ['', 'bool'],
        "title": [],
        "text": [],
        "data": []
    },
    'GradeService': {
        'lineitem': [],
        'lineitems': [],
        'scope':['', 'List[str]']
    },
    'LTIMessage': {
        "iss": [],
        "sub": [],
        "given_name": [],
        "deployment_id": ["https://purl.imsglobal.org/spec/lti/claim/deployment_id"],
        "message_type": ["https://purl.imsglobal.org/spec/lti/claim/message_type"],
        "version": ["https://purl.imsglobal.org/spec/lti/claim/version"],
        "role": ["https://purl.imsglobal.org/spec/lti/claim/roles", "List[str]"],
        "context": ["https://purl.imsglobal.org/spec/lti/claim/context", 'Context'],
        "resource_link": ["https://purl.imsglobal.org/spec/lti/claim/resource_link", 'ResourceLink'],
        "tool_platform": ["https://purl.imsglobal.org/spec/lti/claim/tool_platform", 'ToolPlatform'],
        "launch_presentation": ["https://purl.imsglobal.org/spec/lti/claim/launch_presentation", 'LaunchPresentation'],
        "custom": ["https://purl.imsglobal.org/spec/lti/claim/custom", 'Custom'],
        "deep_linking_settings": ["https://purl.imsglobal.org/spec/lti-dl/claim/deep_linking_settings", 'DeeplinkSettings'],
        "grade_service": ['https://purl.imsglobal.org/spec/lti-ags/claim/endpoint', 'GradeService']
    },
    'DeeplinkResponse': {
        "version": ["https://purl.imsglobal.org/spec/lti/claim/version", "str", "1.3.0"],
        "message_type": ["https://purl.imsglobal.org/spec/lti/claim/message_type", "str", "LTIDeepLinkingResponse"],
        "data": ["https://purl.imsglobal.org/spec/lti-dl/claim/data"],
        "deployment_id": ["https://purl.imsglobal.org/spec/lti/claim/deployment_id"],
        "content_items": ["https://purl.imsglobal.org/spec/lti-dl/claim/content_items", "List"]
    },
    'LineItem': {
        'cls_const': {
            'mime': 'mmm',
            'read_scope': 'xxx',
            'write_scope': 'zzzz'
        },
        'id': [],
        'label': [],
        'scoreMaximum': ['', 'float'],
        'tag': [],
        'resourceId': [],
        'resourceLinkId': [],
        'startDateTime': [],
        'endDateTime': [],
    },
    'GradingProgress': (
        'NotReady',
        'Failed',
        'Pending',
        'PendingManual',
        'FullyGraded'
    ),
    'ActivityProgress' : (
        'Initialized',
        'Started',
        'InProgress',
        'Submitted',
        'Completed'
    ),
    'Score': {
        'userId': [],
        'scoreGiven': ['', 'float'],
        'scoreMaximum': ['', 'float'],
        'comment': [],
        'timestamp': ['', 'datetime'],
        'activityProgress': ['', 'ActivityProgress'],
        'gradingProgress': ['', 'GradingProgress']
    },
    'Result': {
        'userId': [],
        'resultScore': ['', 'float'],
        'resultMaximum': ['', 'float'],
        'comment': [],
        'timestamp': [],
    },
    'LTIResourceLink': {
        'type': ['', 'str', 'ltiResourceLink'],
        'title': [],
        'text': [],
        'url': [],
        'custom': ['', 'Dict[str,str]'],
        'line_item': ['lineItem', 'LineItem'],
        'max_points': ['lineItem:LineItem->scoreMaximum', 'float'],
        'resource_id': ['lineItem:LineItem->resourceId', 'float']
    }
}

template_enum = """
class {name}(Enum):

"""

template_class_val = """
    {name} = '{value}'
"""

template_class = "class {name}(dict):"

template_class_init = """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
"""

template_class_init_val = """
        if not self.get('{long}'):
            self['{long}'] = '{value}'
"""

template_property = """
    @property
    def {short}(self) -> {type}:
        val = self.get('{long}')
        if issubclass({type}, Enum):
            return {type}(val)
        if (isinstance(val, dict) and not isinstance(val, {type})):
            typed_val = {type}( **val )
            self['{long}'] = typed_val
            return typed_val
        return val
            

    @{short}.setter
    def {short}(self, value: {type}):
        if isinstance(value, Enum):
            self['{long}'] = value.value
        else:
            self['{long}'] = value
"""

template_datetime_property = """
    @property
    def {short}(self) -> datetime:
        val = self.get('{long}')
        if (val):
            return datetime.fromisoformat(val)
        return None

    @{short}.setter
    def {short}(self, value: datetime):
        self['{long}'] = value.isoformat()
"""

template_dict_property = """
    @property
    def {short}(self) -> {type}:
        if not '{long}' in self:
            self['{long}'] = {{}}
        return self.get('{long}')

    @{short}.setter
    def {short}(self, value: {type}):
        self['{long}'] = value
"""

template_list_property = """
    @property
    def {short}(self) -> {type}:
        if not '{long}' in self:
            self['{long}'] = []
        return self.get('{long}')

    @{short}.setter
    def {short}(self, value: {type}):
        self['{long}'] = value
"""

template_nested_property = """
    @property
    def {short}(self) -> {type}:
        if self.get('{container}'):
            return self.get('{container}').get('{attr}')

    @{short}.setter
    def {short}(self, value: {type}):
        if not self.get('{container}'):
            self['{container}'] = {container_class}()
        self['{container}']['{attr}'] = value
"""

def generate_enum(name: str, spec: tuple):
    gen = []
    gen.append(template_enum.format(name=name))
    for item in spec:
        gen.append(template_class_val.format(name=item.upper(), value=item))
    return gen


def generate_class(name: str, spec: dict):
    gen = []
    gen.append(template_class.format(name=name))
    init = False
    for (k, v) in spec.items():
        if k=='cls_const':
            for (kk,vv) in v.items():
                gen.append(template_class_val.format(name=kk, value=vv))
        elif len(v) == 3:
            lk = k if len(v) == 0 or len(v[0]) == 0 else v[0]
            if not init:
                gen.append(template_class_init)
            gen.append(template_class_init_val.format(long=lk, value=v[2]))
    items = (item for item in spec.items() if isinstance(item[1], list) )
    for (k, v) in items:
        type = 'str' if len(v) < 2 else v[1]
        lk = k if len(v) == 0 or len(v[0]) == 0 else v[0]
        if '->' in lk:
            ccl, a = lk.split('->')
            c, cl = ccl.split(':')
            gen.append(template_nested_property.format(
                short=k, container=c, attr=a, container_class=cl, type=type))
        elif type.startswith('List'):
            gen.append(template_list_property.format(
                short=k, long=lk, type=type))
        elif type.startswith('Dict'):
            gen.append(template_dict_property.format(
                short=k, long=lk, type=type))
        elif type == 'datetime':
            gen.append(template_datetime_property.format(
                short=k, long=lk))
        else:
            gen.append(template_property.format(short=k, long=lk, type=type))

    if len(gen) == 1:
        gen.append('    pass')
    return gen


if __name__ == "__main__":
    gen = []
    gen.append(
        """
# generated file! see gen_model.py
from typing import List, Set, Dict, Tuple, Optional
from enum import Enum
from datetime import datetime

        """

    )

    for (k, v) in models.items():
        if isinstance(v, dict):
            gen.extend(generate_class(k, v))
        else:
            gen.extend(generate_enum(k, v))
        gen.append('')
        gen.append('')

    with open('lti/gen_model.py', 'w') as model:
        model.writelines([l+'\n' for l in gen])
