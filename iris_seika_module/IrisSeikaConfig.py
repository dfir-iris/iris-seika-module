#!/usr/bin/env python3
#
#  IRIS Seika.io Module Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

module_name = "IrisSeika"
module_description = "Provides an interface between Seika and IRIS"
interface_version = "1.2.0"
module_version = "1.0.0"
pipeline_support = False
pipeline_info = {}

module_configuration = [
    {
        "param_name": "seika_api_key",
        "param_human_name": "Seika API Key",
        "param_description": "API key to use to communicate with Seika.io",
        "default": None,
        "mandatory": True,
        "type": "sensitive_string"
    },
    {
        "param_name": "seika_manual_hook_enabled",
        "param_human_name": "Manual triggers on IOCs",
        "param_description": "Set to True to offers possibility to manually triggers the module via the UI",
        "default": True,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "seika_on_update_hook_enabled",
        "param_human_name": "Triggers automatically on IOC update",
        "param_description": "Set to True to automatically add a Seika insight each time an IOC is updated",
        "default": False,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "seika_on_create_hook_enabled",
        "param_human_name": "Triggers automatically on IOC create",
        "param_description": "Set to True to automatically add a Seika insight each time an IOC is created",
        "default": False,
        "mandatory": True,
        "type": "bool",
        "section": "Triggers"
    },
    {
        "param_name": "seika_ip_assign_countrycode_as_tag",
        "param_human_name": "Assign ASN tag to IP",
        "param_description": "Assign a new tag to IOC IPs with the ASN fetched from Seika",
        "default": True,
        "mandatory": True,
        "type": "bool",
        "section": "Insights"
    },
    {
        "param_name": "seika_report_as_attribute",
        "param_human_name": "Add Seika report as new IOC attribute",
        "param_description": "Creates a new attribute on the IOC, base on the Seika report. Attributes are based "
                             "on the templates of this configuration",
        "default": True,
        "mandatory": True,
        "type": "bool",
        "section": "Insights"
    },
    {
        "param_name": "seika_ip_report_template",
        "param_human_name": "IP report template",
        "param_description": "IP report template used to add a new custom attribute to the target IOC",
        "default": "<div class=\"row\">\n    <div class=\"col-12\">\n        <h3>Basic information</h3>\n        <dl class=\"row\">\n            {% if organization %}\n            <dt class=\"col-sm-3\">Organization</dt>\n            <dd class=\"col-sm-9\">{{ organization }}</dd>\n            {% endif %}\n            \n            {% if location.country_name %}\n            <dt class=\"col-sm-3\">Country</dt>\n            <dd class=\"col-sm-9\">{{ location.country_name }} (location.continent_name )</dd>\n            {% endif %}\n        </dl>\n    </div>\n</div>    \n\n{% if scan %}\n<div class=\"row\">\n    <div class=\"col-12\">\n        <h3>Detected scans</h3>\n        {% for scan in scan %}\n            <dl class=\"row\">\n                <dt class=\"col-sm-3\">Port</dt>\n                <dd class=\"col-sm-9\">{{ scan.port }}</dd>\n                \n                <dt class=\"col-sm-3\">Protocol</dt>\n                <dd class=\"col-sm-9\">{{ scan.protocol }}</dd>\n            </dl>\n            {% endfor %}\n    </div>\n</div>    \n{% endif %}\n\n{% if bruteforce %}\n<div class=\"row\">\n    <div class=\"col-12\">\n        <h3>Bruteforce</h3>\n        {% for bf in bruteforce %}\n            <dl class=\"row\">\n                <dt class=\"col-sm-3\">Port</dt>\n                <dd class=\"col-sm-9\">{{ bf.port }}</dd>\n                \n                <dt class=\"col-sm-3\">Service</dt>\n                <dd class=\"col-sm-9\">{{ bf.service }}</dd>\n            </dl>\n            {% endfor %}\n    </div>\n</div>    \n{% endif %}\n\n{% if exploitation %}\n<div class=\"row\">\n    <div class=\"col-12\">\n        <h3>Exploitation</h3>\n        {% for ex in exploitation %}\n            <dl class=\"row\">\n                <dt class=\"col-sm-3\">Product</dt>\n                <dd class=\"col-sm-9\">{{ ex.product }}</dd>\n                \n                <dt class=\"col-sm-3\">CVE</dt>\n                <dd class=\"col-sm-9\">{{ ex.cve }}</dd>\n            </dl>\n            {% endfor %}\n    </div>\n</div>    \n{% endif %}",
        "mandatory": False,
        "type": "textfield_html",
        "section": "Templates"
    }
]