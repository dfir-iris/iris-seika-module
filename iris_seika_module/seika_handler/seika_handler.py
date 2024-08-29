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
import logging
import traceback

import iris_interface.IrisInterfaceStatus as InterfaceStatus
from app.datamgmt.manage.manage_attribute_db import add_tab_attribute_field

from iris_seika_module.seika_handler.seika_helper import gen_ip_report_from_template, get_seika_host_info


class SeikaHandler(object):
    def __init__(self, mod_config, server_config, logger):
        self.mod_config = mod_config
        self.server_config = server_config
        self.log = logger
        self.apiKey = self.mod_config.get('seika_api_key')

    def tag_if_friendly_and_bf_scan(self, context, ioc):
        """
        Tag an IOC if the IP is considered friendly and contains scan or bruteforce
        :param ioc: IOC checked
        :param context: Seika.io report
        :return:
        """

        if ioc.ioc_tags is None:
            ioc.ioc_tags = ""

        if context.get('friendly') is True:
            if f'seika:friendly' not in ioc.ioc_tags.split(','):
                ioc.ioc_tags = f"{ioc.ioc_tags},seika:friendly"
        else:
            if f'seika:friendly' in ioc.ioc_tags.split(','):
                ioc.ioc_tags = ioc.ioc_tags.replace('seika:friendly', '').replace(',,', '')

        if 'scan' in context:
            if f'seika:scan' not in ioc.ioc_tags.split(','):
                ioc.ioc_tags = f"{ioc.ioc_tags},seika:scan"
        else:
            if f'seika:scan' in ioc.ioc_tags.split(','):
                ioc.ioc_tags = ioc.ioc_tags.replace('seika:scan', '').replace(',,', '')

        if 'exploitation' in context:
            if f'seika:exploit' not in ioc.ioc_tags.split(','):
                ioc.ioc_tags = f"{ioc.ioc_tags},seika:exploit"
        else:
            if f'seika:exploit' in ioc.ioc_tags.split(','):
                ioc.ioc_tags = ioc.ioc_tags.replace('seika:exploit', '').replace(',,', '')

        if 'bruteforce' in context:
            if f'seika:bruteforce' not in ioc.ioc_tags.split(','):
                ioc.ioc_tags = f"{ioc.ioc_tags},seika:bruteforce"
        else:
            if f'seika:bruteforce' in ioc.ioc_tags.split(','):
                ioc.ioc_tags = ioc.ioc_tags.replace('seika:bruteforce', '').replace(',,', '')


    def handle_seika_ip(self, ioc):
        """
        Handles an IOC of type IP and adds Seika.io insights

        :param ioc: IOC instance
        :return: IIStatus
        """

        self.log.info(f'Getting IP report for {ioc.ioc_value}')
        report = get_seika_host_info(ioc.ioc_value, self.apiKey)

        if report.is_failure():
            if report.get_data() == "404":
                self.log.info('No information found for this IP')
                return InterfaceStatus.I2Success("No information found for this IP")

            return report

        results = report.get_data()

        self.tag_if_friendly_and_bf_scan(context=results, ioc=ioc)

        if self.mod_config.get('seika_ip_assign_countrycode_as_tag') is True:
            self.log.info('Assigning new country code tag to IOC.')

            location = results.get('location')
            country_code = location.get('country_code')
            if country_code is None:
                self.log.info('Country code was nul - skipping')

            if ioc.ioc_tags is None:
                ioc.ioc_tags = ""

            if f'seika:{country_code}' not in ioc.ioc_tags.split(','):
                ioc.ioc_tags = f"{ioc.ioc_tags},seika:{country_code}"
            else:
                self.log.info('Country already tagged for this IOC. Skipping')

        if self.mod_config.get('seika_report_as_attribute') is True:
            self.log.info('Adding new attribute Seika.io IP Report to IOC')

            status = gen_ip_report_from_template(html_template=self.mod_config.get('seika_ip_report_template'),
                                                 seika_report=results)

            if not status.is_success():
                return status

            rendered_report = status.get_data()

            try:
                add_tab_attribute_field(ioc, tab_name='Seika.io Report', field_name="HTML report", field_type="html",
                                        field_value=rendered_report)

            except Exception:
                print(traceback.format_exc())
                self.log.error(traceback.format_exc())
                return InterfaceStatus.I2Error(traceback.format_exc())
        else:
            self.log.info('Skipped adding attribute report. Option disabled')

        return InterfaceStatus.I2Success("Successfully processed IP")
