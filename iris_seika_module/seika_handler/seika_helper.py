import json
import traceback

from jinja2 import Template
import logging
from iris_interface import IrisInterfaceStatus

from iris_seika_module.seika_handler.api_handler import send_api_request

log = logging.getLogger('iris_seika_module.seika_helper')


def get_detected_urls_ratio(report):
    avg_urls_detect_ratio = None
    avg_urls_detect_ratio_str = "No information"
    nb_detected_urls = None
    if "detected_urls" in report:
        nb_detected_urls = len(report["detected_urls"])
        count_total = 0
        count_positives = 0

        for detected_url in report["detected_urls"]:
            count_total += detected_url.get('total')
            count_positives += detected_url.get('positives')

        if nb_detected_urls > 0:
            avg_urls_detect_ratio_str = f"{round(count_positives/nb_detected_urls, 2)} / " \
                                              f"{count_total/nb_detected_urls}"

            avg_urls_detect_ratio = round(count_positives/count_total, 2)*100

    return avg_urls_detect_ratio_str, avg_urls_detect_ratio, nb_detected_urls


def gen_domain_report_from_template(html_template, seika_report) -> IrisInterfaceStatus:
    """
    Generates an HTML report for domains, displayed as an attribute in the IOC

    :param html_template: A string representing the HTML template
    :param seika_report: The JSON report fetched with Seika.io API
    :return: IrisInterfaceStatus
    """
    template = Template(html_template)
    context = seika_report
    results = context.get('results')

    context["avg_urls_detect_ratio"], _, context["nb_detected_urls"] = get_detected_urls_ratio(results)

    if "detected_downloaded_samples" in results:
        context["nb_detected_samples"] = len(results["detected_downloaded_samples"])
        count_total = 0
        count_positives = 0

        for samples in results["detected_downloaded_samples"]:
            count_total += samples.get('total')
            count_positives += samples.get('positives')

        if context['nb_detected_samples'] > 0:
            context["avg_samples_detect_ratio"] = f"{round(count_positives/context['nb_detected_samples'], 2)} / " \
                                                  f"{count_total/context['nb_detected_samples']}"
        else:
            context["avg_samples_detect_ratio"] = "No information"

    try:

        rendered = template.render(context)

    except Exception:
        log.error(traceback.format_exc())
        return IrisInterfaceStatus.I2Error(traceback.format_exc())

    return IrisInterfaceStatus.I2Success(data=rendered)


def gen_ip_report_from_template(html_template, seika_report) -> IrisInterfaceStatus:
    """
    Generates an HTML report for IP, displayed as an attribute in the IOC

    :param html_template: A string representing the HTML template
    :param seika_report: The JSON report fetched with Seika.io API
    :return: IrisInterfaceStatus
    """
    template = Template(html_template)
    context = seika_report

    try:

        rendered = template.render(context)

    except Exception:
        print(traceback.format_exc())
        log.error(traceback.format_exc())
        return IrisInterfaceStatus.I2Error(traceback.format_exc())

    return IrisInterfaceStatus.I2Success(data=rendered)


def gen_hash_report_from_template(html_template, seika_report) -> IrisInterfaceStatus:
    """
    Generates an HTML report for hash, displayed as an attribute in the IOC

    :param html_template: A string representing the HTML template
    :param seika_report: The JSON report fetched with Seika.io API
    :return: IrisInterfaceStatus
    """
    template = Template(html_template)
    context = seika_report

    try:

        rendered = template.render(context)

    except Exception:
        print(traceback.format_exc())
        log.error(traceback.format_exc())
        return IrisInterfaceStatus.I2Error(traceback.format_exc())

    return IrisInterfaceStatus.I2Success(data=rendered)


def get_seika_host_info(host: str, api_key: str) -> IrisInterfaceStatus:
    """
    Get information about a host from Seika.io API

    :param host: Host to look up
    :return: Dict with host info
    """

    try:
        response = send_api_request(api_endpoint=f"https://api.seika.io/api/v1/seika/host/{host}",
                                    api_key=api_key)

        if response.ok:
            return IrisInterfaceStatus.I2Success(data=json.loads(response.text))

        # Else if 404
        elif response.status_code == 404:
            return IrisInterfaceStatus.I2Error(message="Host not found", data="404")

        else:
            return IrisInterfaceStatus.I2Error(data=response.text)

    except Exception as e:
        log.error(f"An error occurred: {e}")
        return IrisInterfaceStatus.I2Error(data=str(e))
