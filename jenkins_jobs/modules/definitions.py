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
import logging

logger = logging.getLogger(__name__)


def scm(parser, xml_parent, data):
    xml_parent.set('class', 'org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition')

    type = 'git'
    if 'type' in data:
        type = data.get('type')

    scmModule = __import__('jenkins_jobs.modules.scm', fromlist=type)
    scmHandler = getattr(scmModule, type)
    scmHandler(parser, xml_parent, data)


def script(parser, xml_parent, data):
    XML.SubElement(xml_parent, 'scriptPath').text = data.get('filename')

def inline(parser, xml_parent, data):
    xml_parent.set('class', 'org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition')
    XML.SubElement(xml_parent, 'script').text = data


class Definitions(jenkins_jobs.modules.base.Base):
    sequence = 70

    component_type = 'definition'
    component_list_type = 'definitions'

    def gen_xml(self, parser, xml_parent, data):
        if xml_parent.tag == 'flow-definition':
            publishers = XML.SubElement(xml_parent, 'definition')
            publishers.set('plugin', 'workflow-cps@1.8')

            for action in data.get('definitions', []):
                self.registry.dispatch(
                    'definition',
                    parser,
                    publishers,
                    action
                )
