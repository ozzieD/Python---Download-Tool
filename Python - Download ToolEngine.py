"""
AyxPlugin (required) has-a IncomingInterface (optional).
Although defining IncomingInterface is optional, the interface methods are needed if an upstream tool exists.
"""

import AlteryxPythonSDK as Sdk
import xml.etree.ElementTree as Et
import requests


class AyxPlugin:
    """
    Implements the plugin interface methods, to be utilized by the Alteryx engine to communicate with this plugin.
    Prefixed with "pi", the Alteryx engine will expect the below five interface methods to be defined.
    """

    def __init__(self, n_tool_id: int, alteryx_engine: object, output_anchor_mgr: object):
        """
        Constructor is called whenever the Alteryx engine wants to instantiate an instance of this plugin.
        :param n_tool_id: The assigned unique identification for a tool instance.
        :param alteryx_engine: Provides an interface into the Alteryx engine.
        :param output_anchor_mgr: A helper that wraps the outgoing connections for a plugin.
        """

        # Default properties
        self.n_tool_id = n_tool_id
        self.alteryx_engine = alteryx_engine
        self.output_anchor_mgr = output_anchor_mgr

        # HTTP Action page
        self.http_action = None
        self.radio_URL_man = None
        self.radio_URL_field = None
        self.url_field = None
        self.url_manual = None

        # Headers Page
        self.radio_headers_no = None
        self.radio_headers_man = None
        self.radio_headers_field = None
        self.headers_field = None
        self.headers_manual = None

        # Payload Page
        self.radio_payload_no = None
        self.radio_payload_man = None
        self.radio_payload_field = None
        self.payload_field = None
        self.payload_manual = None

        # Credentials Page
        self.radio_credentials_no = None
        self.radio_credentials_man = None
        self.radio_credentials_field = None
        self.radio_credentials_winauth = None
        self.username_field = None
        self.password_field = None
        self.username_manual = None
        self.password_manual = None

        # Additional Options Page

        # Output anchors
        self.request_output_anchor = None
        self.outputdata_output_anchor = None
        self.headers_output_anchor = None

        # Input anchor
        self.single_input = None

    def pi_init(self, str_xml: str):
        """
        Handles input data verification.
        Called when the Alteryx engine is ready to provide the tool configuration from the GUI.
        :param str_xml: The raw XML from the GUI.
        """

        # Obtaining the user inputs from the GUI from the config xml

        # HTTP Action
        self.http_action = Et.fromstring(str_xml).find('HTTPAction').text if 'HTTPAction' in str_xml else None
        self.radio_URL_man = Et.fromstring(str_xml).find('radioURLMan').text if 'radioURLMan' in str_xml else None
        self.radio_URL_field = Et.fromstring(str_xml).find('radioURLField').text if 'radioURLField' in str_xml else None
        self.url_field  = Et.fromstring(str_xml).find('URLDrop').text if 'URLDrop' in str_xml else None
        self.url_manual = Et.fromstring(str_xml).find('URLText').text if 'URLText' in str_xml else None

        print(self.http_action,
              self.radio_URL_man,
              self.radio_URL_field,
              self.url_field,
              self.url_manual)

        # Headers
        self.radio_headers_no = Et.fromstring(str_xml).find('radioHeadersNo').text if 'radioHeadersNo' in str_xml else None
        self.radio_headers_man = Et.fromstring(str_xml).find('radioHeadersMan').text if 'radioHeadersMan' in str_xml else None
        self.radio_headers_field = Et.fromstring(str_xml).find('radioHeadersField').text if 'radioHeadersField' in str_xml else None
        self.headers_field = Et.fromstring(str_xml).find('headerFieldsList').text if 'headerFieldsList' in str_xml else None
        self.headers_manual = Et.fromstring(str_xml).find('headersText').text if 'headersText' in str_xml else None

        print(
              self.radio_headers_man,
              self.radio_headers_field,
              self.headers_field,
              self.headers_manual)

        # Payload
        self.radio_payload_no = Et.fromstring(str_xml).find('radioPayloadNo').text if 'radioPayloadNo' in str_xml else None
        self.radio_payload_man = Et.fromstring(str_xml).find('radioPayloadMan').text if 'radioPayloadMan' in str_xml else None
        self.radio_payload_field = Et.fromstring(str_xml).find('radioPayloadField').text if 'radioPayloadField' in str_xml else None
        self.payload_field = Et.fromstring(str_xml).find('payloadFieldDrop').text if 'payloadFieldDrop' in str_xml else None
        self.payload_manual = Et.fromstring(str_xml).find('payloadText').text if 'payloadText' in str_xml else None

        print(
              self.radio_payload_man,
              self.radio_payload_field,
              self.payload_field,
              self.payload_manual)

        # Credentials
        self.radio_credentials_no = Et.fromstring(str_xml).find('radioCredentialsNo').text if 'radioCredentialsNo' in str_xml else None
        self.radio_credentials_man = Et.fromstring(str_xml).find('radioCredentialsMan').text if 'radioCredentialsMan' in str_xml else None
        self.radio_credentials_field = Et.fromstring(str_xml).find('radioCredentialsField').text if 'radioCredentialsField' in str_xml else None
        self.radio_credentials_winauth = Et.fromstring(str_xml).find('radioCredentialsWinAuth').text if 'radioCredentialsWinAuth' in str_xml else None
        self.username_field = Et.fromstring(str_xml).find('UserDrop').text if 'UserDrop' in str_xml else None
        self.username_manual = Et.fromstring(str_xml).find('UserText').text if 'UserText' in str_xml else None
        self.password_field = Et.fromstring(str_xml).find('PassDrop').text if 'PassDrop' in str_xml else None
        self.password_manual = Et.fromstring(str_xml).find('PassText').text if 'PassText' in str_xml else None

        print(
              self.radio_headers_man,
              self.radio_headers_field,
              self.radio_credentials_winauth,
              self.headers_field,
              self.headers_manual)

        # Obtaining the output anchors from the config xml
        self.request_output_anchor = self.output_anchor_mgr.get_output_anchor('Request')
        self.outputdata_output_anchor = self.output_anchor_mgr.get_output_anchor('OutputData')
        self.headers_output_anchor = self.output_anchor_mgr.get_output_anchor('Headers')


    def pi_add_incoming_connection(self, str_type: str, str_name: str) -> object:
        """
        The IncomingInterface objects are instantiated here, one object per incoming connection, also pre_sort() is called here.
        Called when the Alteryx engine is attempting to add an incoming data connection.
        :param str_type: The name of the input connection anchor, defined in the Config.xml file.
        :param str_name: The name of the wire, defined by the workflow author.
        :return: The IncomingInterface object(s).
        """

        self.single_input = IncomingInterface(self)
        return self.single_input

    def pi_add_outgoing_connection(self, str_name: str) -> bool:
        """
        Called when the Alteryx engine is attempting to add an outgoing data connection.
        :param str_name: The name of the output connection anchor, defined in the Config.xml file.
        :return: True signifies that the connection is accepted.
        """

        return True

    def pi_push_all_records(self, n_record_limit: int) -> bool:
        """
        Called when a tool has no incoming data connection.
        :param n_record_limit: Set it to <0 for no limit, 0 for no records, and >0 to specify the number of records.
        :return: True for success, False for failure.
        """
        #
        # print(type(self.radio_URL_man), type(self.url_manual))
        # print(bool(self.url_manual))

        if self.radio_URL_field == 'True' and not bool(self.url_field):
            self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, self.xmsg('Missing URL. Please Enter a URL!'))
            print('Field conditional')

        if self.radio_URL_man == 'True' and not bool(self.url_manual):
            print(bool(self.url_manual))
            self.alteryx_engine.output_message(self.n_tool_id, Sdk.EngineMessageType.error, self.xmsg('Missing URL. Please Enter a URL!'))
            print('Manual conditional')

        self.record_info_out_all = self.build_record_info_out()

        self.request_output_anchor.init(self.record_info_out_all[0])
        self.outputdata_output_anchor.init(self.record_info_out_all[1])
        self.headers_output_anchor.init(self.record_info_out_all[2])

        self.downloaded_data = self.get_download_data()


        return False

    def pi_close(self, b_has_errors: bool):
        """
        Called after all records have been processed.
        :param b_has_errors: Set to true to not do the final processing.
        """
        pass

    def xmsg(self, msg_string: str):
        """
        A non-interface, non-operational placeholder for the eventual localization of predefined user-facing strings.
        :param msg_string: The user-facing string.
        :return: msg_string
        """

        return msg_string

    def build_record_info_out(self):
        """
        A non-interface helper for pi_push_all_records() responsible for creating the outgoing record layout.
        :return: The outgoing record layout, otherwise nothing.
        """

        record_info_out_request = Sdk.RecordInfo(self.alteryx_engine)
        record_info_out_outputdata = Sdk.RecordInfo(self.alteryx_engine)
        record_info_out_headers = Sdk.RecordInfo(self.alteryx_engine)

        record_info_out_request.add_field('Request', Sdk.FieldType.v_wstring, 999999)
        record_info_out_outputdata.add_field('Output Data', Sdk.FieldType.v_wstring, 999999)
        record_info_out_headers.add_field('Headers', Sdk.FieldType.v_wstring, 999999)

        return [record_info_out_request, record_info_out_outputdata, record_info_out_headers]


    def get_download_data(self): # May turn into a class
        if self.radio_URL_field == 'True':
            url = self.url_field # TODO figure out field extraction for Incoming interface object
        else:
            url = self.url_manual

        if self.radio_headers_field == 'True':
            headers = self.headers_field # TODO figure out field extraction for Incoming interface object
        elif self.headers_manual == 'True':
            headers = self.headers_manual
        else:
            headers = None

        if self.radio_payload_field == 'True':
            payload = self.payload_field  # TODO figure out field extraction for Incoming interface object
        elif self.payload_manual == 'True':
            payload = self.payload_manual
        else:
            payload = None

        if self.radio_credentials_field == 'True':
            username = self.username_field # TODO figure out field extraction for Incoming interface object
            password = self.password_field
        elif self.radio_credentials_man == 'True':
            username = self.username_manual
            password = self.password_manual
        elif self.radio_credentials_winauth == 'True': # TODO do somthing with this
            test = 'Something'
        else:
            username = None
            password =None

        # TODO: Advanced Options
        pass

class IncomingInterface:
    """
    This optional class is returned by pi_add_incoming_connection, and it implements the incoming interface methods, to
    be utilized by the Alteryx engine to communicate with a plugin when processing an incoming connection.
    Prefixed with "ii", the Alteryx engine will expect the below four interface methods to be defined.
    """

    def __init__(self, parent: object):
        """
        Constructor for IncomingInterface.
        :param parent: AyxPlugin
        """

        # Default properties
        self.parent = parent

        # Custom properties
        self.record_info_in = None
        self.record_info_out = None

    def ii_init(self, record_info_in: object) -> bool:
        """
        Handles setting up the outgoing record layout.
        Called to report changes of the incoming connection's record metadata to the Alteryx engine.
        :param record_info_in: A RecordInfo object for the incoming connection's fields.
        :return: True for success, otherwise False.
        """

        if self.parent.field_selection is None:
            self.parent.alteryx_engine.output_message(self.parent.n_tool_id, Sdk.EngineMessageType.error, self.parent.xmsg('Select a field.'))
            return False

        self.record_info_in = record_info_in  # For later reference.

        # Storing the user selected field to use in ii_push_record, to avoid repeated field lookup.
        self.target_field = self.record_info_in[
            self.record_info_in.get_field_num(self.parent.field_selection)
        ]

        self.record_info_out = self.record_info_in.clone()  # Creating an exact copy of record_info_in.

        # Initialize output anchors
        self.parent.unique_output_anchor.init(self.record_info_out)
        self.parent.dupe_output_anchor.init(self.record_info_out)
        return True

    def ii_push_record(self, in_record: object) -> bool:
        """
        Responsible for pushing records out, upon evaluation of the record data being passed from the sorted field,
        to see if it equals to the previous data.
        Called when an input record is being sent to the plugin.
        :param in_record: The data for the incoming record.
        :return: True
        """

        current_value = self.target_field.get_as_string(in_record)

        if current_value == self.previous_value:
            self.parent.dupe_output_anchor.push_record(in_record)
        else:
            self.parent.unique_output_anchor.push_record(in_record)

        self.previous_value = current_value
        return True

    def ii_update_progress(self, d_percent: float):
        """
        Called by the upstream tool to report what percentage of records have been pushed.
        :param d_percent: Value between 0.0 and 1.0.
        """

        # Inform the Alteryx engine of the tool's progress.
        self.parent.alteryx_engine.output_tool_progress(self.parent.n_tool_id, ((d_percent/2)+0.5))

        # Inform the outgoing connections of the tool's progress.
        self.parent.unique_output_anchor.update_progress(d_percent)
        self.parent.dupe_output_anchor.update_progress(d_percent)

    def ii_close(self):
        """
        Responsible for outputting the final count of unique and duplicates as a message, and closing out both anchors.
        Called when the incoming connection has finished passing all of its records.
        """

        self.parent.alteryx_engine.output_message(
            self.parent.n_tool_id,
            Sdk.EngineMessageType.info,
            self.parent.xmsg('{} unique records and {} dupes were found'.format(self.records_unique, self.records_dupe))
        )

        # Close outgoing connections.
        self.parent.unique_output_anchor.close()
        self.parent.dupe_output_anchor.close()
