import xml.etree.ElementTree as ET
import argparse
import os

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Add SplunkAppender to log4j xml script"
    )

    # Add the parameters positional/optional
    parser.add_argument("-i", "--input_file", required=True, type=str)
    parser.add_argument("-o", "--output_file", required=True, type=str)

    # Parse the arguments
    args = parser.parse_args()
    print(args)

    tree = ET.parse(args.input_file)
    root = tree.getroot()
    appenders = root.find("Appenders")
    root_logger = root.find("Loggers").find("Root")

    splunk_appender = ET.Element("SplunkHttp", 
        {
            "name": "splunk",
            "url": "${env:SPLUNK_HEC_URL}",
            "token": "${env:SPLUNK_HEC_TOKEN}",
            "index": "your_splunk_index",
            "host": "databricks",
            "disableCertificateValidation": "true",
            "eventBodySerializer": "HecJsonSerializer"
        }
    )
    pattern = ET.SubElement(splunk_appender, "PatternLayout", {"pattern": "%m"})
    splunk_appender_ref = ET.Element("AppenderRef", {"ref": "splunk"})

    appenders.insert(-1, splunk_appender)
    root_logger.insert(-1, splunk_appender_ref)


    tree.write(args.output_file)