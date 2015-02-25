#!/usr/bin/env python3.4

# Copyright 2015 NEC Corporation.                                          #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#   http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #

# $ sudo pip3 install redis
# $ sudo pip3 install msgpack-python

import redis
import msgpack
from io import BytesIO
import traceback
from copy import copy

class Monitor:
    """
    Generates a message sequence diagram by tapping Redis server.
    """

    TYPE_REQUEST = 0
    TYPE_RESPONSE = 1
    TYPE_EVENT = 2
    TYPE_REFLECTED_EVENT = 99

    REQUEST = 'REQUEST' 
    RESPONSE = 'RESPONSE'
    EVENT = 'EVENT' 

    REFLECTED_EVENT_PATTERN = 'reflected_event'
    REFLECTED_EVENT_PATTERN_BYTE = b'reflected_event'

    GET_RIGHT =     '----- GET ---->'
    GET_LEFT =      '<---- GET -----'
    POST_RIGHT =    '----- POST --->'
    POST_LEFT =     '<--- POST -----'
    PUT_RIGHT =     '----- PUT ---->'
    PUT_LEFT =      '<---- PUT -----'
    DELETE_RIGHT =  '---- DELETE -->'
    DELETE_LEFT =   '<-- DELETE ----'
    RESPONSE_RIGHT =    '----- {} ---->'
    RESPONSE_LEFT =     '<---- {} -----'
    EVENT_RIGHT =       '---- EVENT --->'
    EVENT_LEFT =        '<--- EVENT ----'
    BAR =         '---------------'  
    EMPTY =       '               '  
    REQUEST_LEFT = {'GET': GET_LEFT,  'POST': POST_LEFT, 'PUT': PUT_LEFT, 'DELETE': DELETE_LEFT}
    REQUEST_RIGHT = {'GET': GET_RIGHT, 'POST': POST_RIGHT, 'PUT': PUT_RIGHT, 'DELETE': DELETE_RIGHT}

    BODY_SUMMARY = '{} {} {}'
    BODY_SUMMARY_EVENT = '{} {}'

    def __init__(self, *args, **kwargs):
        '''
        Writes sequence diagram header    
       
        0         1         2         3         4
        01234567890123456789012345678901234567890
         4-3             4+16-3          4+16*2-3
         object1         object2         object3
            |               |<- REQUEST ----|   0 REQUEST GET sno path [body]
            |<--------------|               |   1 REQUEST GET sno path [body]
            |-------------->|               |   2 200 OK path sno [body]
            |               |-- RESPONSE -->|   3 200 OK path sno [body]
            |-- EVENT --------------------->|   4 EVENT [body]
             
        <html>
        <header></header>
        <body>
        <a name="0">
        <pre>
        serial: 0
        REQUEST GET (10) [path]
        
        body in JSON
        </pre>
        <a name="1">
        <pre>
        serial: 1
        200 OK (10) [path]
        
        body in JSON
        </pre>
        </body>
                   
        '''
        self.object_ids = kwargs['object_ids']
        self.output = kwargs['output']
        if 'hyperlink' in kwargs:
            self.hyperlink = kwargs['hyperlink']
        else:
            self.hyperlink = False
        self.serial = 0
        object_number = len(self.object_ids)
        c = 0
        cc = 0
        self.header_format = ' '
        self.arrow_default = [] 
        self.vertical_lines_format = '    ' 
        for count in range(object_number):
            #self.header_format += '{'+str(c)+':<16}'  
            self.header_format += '{:<16}'  
            c += 1
            if count < object_number - 1:
                #self.vertical_lines_format += '{'+str(cc)+'}{'+str(cc+1)+':<15}'
                self.vertical_lines_format += '{}{:<15}'
                self.arrow_default.append('|')
                self.arrow_default.append(Monitor.EMPTY)
            else:
                #self.vertical_lines_format += '{'+str(cc)+'}'
                self.vertical_lines_format += '{}'
                self.arrow_default.append('|')
            cc += 2
        self.output(self.header_format.format(*self.object_ids))

    def start(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        p = r.pubsub(ignore_subscribe_messages=True)
        p.psubscribe('*') 
        while True:  # inifinite loop
            for msg in p.listen(): # blocks untile new message is received.
                #pattern = msg['pattern']
                type_ = msg['type'] # Redis message type
                dstid = msg['channel'].decode(encoding='utf-8') # Redis pubsub channel  # Destination
                if type_ != 'message' and type_ != 'pmessage':
                        continue
                else: # subscribed events
                    try:
                        bio = BytesIO()
                        bio.write(msg['data'])
                        bio.seek(0)
                        upk = msgpack.Unpacker(bio)
                        tp = upk.unpack()  # Message type
                        sno = upk.unpack()  # Serial number assigned by MessageDispatcher
                        srcid = upk.unpack().decode('ascii')  # Source
                        body = upk.unpack()
                        method = None
                        path = None
                        status = None
                        subscriber_id = None
                        publisher_id = None
                        event_type = None
                        message_type = '*'
                        if tp == Monitor.TYPE_REQUEST:
                            message_type = Monitor.REQUEST
                            method = body[1].decode('ascii')
                            path = '/{}/{}'.format(body[0].decode('ascii'), body[2].decode('ascii'))
                            self._write_sequence(self.serial, message_type, dstid, srcid, sno, path, method, status, event_type, body)
                            self.serial += 1
                        elif tp == Monitor.TYPE_RESPONSE:
                            message_type = Monitor.RESPONSE
                            status = body[0]
                            path = '' 
                            self._write_sequence(self.serial, message_type, dstid, srcid, sno, path, method, status, event_type, body)
                            self.serial += 1
                        elif tp == Monitor.TYPE_REFLECTED_EVENT:
                            message_type = Monitor.EVENT
                            dstid = srcid
                            srcid = body[0].decode('ascii')
                            event_type = body[1].decode('ascii')
                            self._write_sequence(self.serial, message_type, dstid, srcid, sno, path, method, status, event_type, body)
                            self.serial += 1
                        #print('serial: {}, type: {}, dstid: {}, srcid: {}: sno: {}'.format(self.serial, message_type, dstid, srcid, sno))
                        #print('serial: {}, type: {}, dstid: {}, srcid: {}: sno: {}, data: {}'.format(self.serial, message_type, dstid, srcid, sno, body))
                        #print('')
                    except:
                        traceback.print_exc()
                        pass


    def _write_sequence(self, serial, message_type, dstid, srcid, sno, path, method, status, event_type, body):
        '''
        Writes sequence
        '''
        object_number = len(self.object_ids)
        
        dstid_idx = -1 
        srcid_idx = -1

        if dstid in self.object_ids:
            dstid_idx = self.object_ids.index(dstid)
        if srcid in self.object_ids:
            srcid_idx = self.object_ids.index(srcid)
        #print(dstid)
        #print(srcid)
        #print('--')
        if (dstid_idx < 0) or (srcid_idx < 0):
            pass
        else:

            arrow = copy(self.arrow_default)

            left = None
            right = None
            if message_type == Monitor.REQUEST:
                left = Monitor.REQUEST_LEFT[method]
                right = Monitor.REQUEST_RIGHT[method]
            elif message_type == Monitor.RESPONSE:
                left = Monitor.RESPONSE_LEFT.format(status)
                right = Monitor.RESPONSE_RIGHT.format(status)
            elif message_type == Monitor.EVENT:
                left = Monitor.EVENT_LEFT
                right = Monitor.EVENT_RIGHT

            if (dstid_idx > srcid_idx):  # Drows an arrow to the right
                c = srcid_idx
                for count in range(srcid_idx, dstid_idx):
                    C = c * 2
                    if c == srcid_idx and dstid_idx - srcid_idx > 1:
                        arrow[C+1] = Monitor.BAR
                    elif c == srcid_idx and dstid_idx - srcid_idx == 1:
                        arrow[C+1] = right
                    elif c == dstid_idx - 1:
                        arrow[C] = '-'
                        arrow[C+1] = right 
                        break
                    else:
                        arrow[C] = '-' 
                        arrow[C+1] = Monitor.BAR 
                    c += 1 
            else:  # Draws an arrow to the left
                c = dstid_idx
                for count in range(dstid_idx, srcid_idx):
                    C = c * 2
                    if c == dstid_idx:
                        arrow[C+1] = left
                    elif c == srcid_idx:
                        arrow[C] = '-'
                        arrow[C+1] = Monitor.BAR 
                        break
                    else:
                        arrow[C] = '-'
                        arrow[C+1] = Monitor.BAR 
                    c += 1 

            if (message_type == Monitor.EVENT):
                arrow.append(event_type)
                final_format = self.vertical_lines_format+'  '+Monitor.BODY_SUMMARY_EVENT 
            else:
                arrow.append(sno)
                arrow.append(path)
                final_format = self.vertical_lines_format+'  '+Monitor.BODY_SUMMARY
            if self.hyperlink:
                # TODO: hyperlink generation to obtain body detail
                arrow.append(',http://localhost:10082/?serial=1234')
            else:
                arrow.append('')
            self.output(final_format.format(*arrow))

if __name__ == '__main__':
    
    kwargs = {}
    kwargs['object_ids'] = ['resttranslator', 'systemmanager', 'romgr1', 'gen', 'network1', 'aggre', 'network0', 'lsw'] 
    kwargs['output'] = print 
    monitor = Monitor(**kwargs)
    monitor.start()


