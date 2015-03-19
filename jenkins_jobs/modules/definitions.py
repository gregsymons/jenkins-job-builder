# Copyright 2015 Gil Forcada Codinachs <gforcada@gnome.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
LATER
"""


import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base


def scm(parser, xml_parent, data):
    from jenkins_jobs.modules.scm import git
    git(parser, xml_parent, data)


def script(parser, xml_parent, data):
    XML.SubElement(xml_parent, 'scriptPath').text = data.get('filename')


class Definitions(jenkins_jobs.modules.base.Base):
    sequence = 70

    component_type = 'definition'
    component_list_type = 'definitions'

    def gen_xml(self, parser, xml_parent, data):
        if xml_parent.tag == 'flow-definition':
            publishers = XML.SubElement(xml_parent, 'definition')

            for action in data.get('definitions', []):
                self.registry.dispatch(
                    'definition',
                    parser,
                    publishers,
                    action
                )
