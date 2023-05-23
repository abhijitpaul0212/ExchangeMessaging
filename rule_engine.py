# coding: utf-8

import random


class RuleEngine:
    """
    Rule Engine Class contains programmatic approach to handle, process and generate various
    outbound messages depending on the inbound messages
    """
    
    def read_message_from_textfile(self, filename) -> str:
        """This method reads data from text file

        Args:
            filename (text file): Text file name

        Returns:
            string: Text file data
        """
        data = ""
        file_path = "./" + filename
        with open(file_path, "r") as f:
            for line in f.readlines():
                data = data + "".join(line)
        return data
    
    def convert_to_dict(self, data) -> dict:
        """This method reads data in string pipe delimited format and converts it into dictionary dataset

        Args:
            data (string): Pipe delimited inbound dataset

        Returns:
            dict: Dataset
        """
        data_dic = {}
        data = data.split("|")
        for i in data:
            i = i.split(":")
            i[0] = i[0].replace('\n', '').strip()
            i[1] = i[1].replace('\n', '').strip()
            data_dic[i[0]] = i[1]
        return data_dic

    def generate_order_id(self) -> None:
        """
        This method generate order_id of 5 digit length
        """
        global ORDER_ID
        ORDER_ID = random.randint(10000,99999)

    def construct_reject(self, data, prefix="") -> str:
        """This method constructs pipe delimited string for reject message

        Args:
            data (dict): This is a parsed and converted exchange message data

        Returns:
            string: pipe demilited string message
        """
        nl = '\n'
        converted =  f"ResponseType:REJECT|OrderID:{data['OrderID']}|Symbol:{data.get('Symbol')}|Side:{data.get('Side')}{nl}|Price:{data.get('Price')}|Quantity:{data.get('Quantity')}|AccountID:{data.get('Account')}|ErrorCode:100109{nl}|TimeStamp:{data.get('TimeStamp')}|Exchange_Order_Id:{ORDER_ID}|ChildResponseType:CANCEL_ORDER_REJECT_MIDDLE{nl}|Duration:{data.get('Duration')}|ExchTs:{data.get('TimeStamp')}"
        
        filename = prefix + "reject.txt"
        file_path = "./outbound_messages/" + filename
        print("Generating REJECT message")
        with open(file_path, "w") as f:
            f.write(converted)
            f.close()
        
        return converted

    def construct_trade_confirm(self, data, prefix="") -> str:
        """This method constructs pipe delimited string for trade confirm message

        Args:
            data (dict): This is a parsed and converted exchange message data

        Returns:
            string: pipe demilited string message
        """
        nl = '\n'
        converted =  f"ResponseType:TRADE_CONFIRM|OrderID:{data['OrderID']}|Symbol:{data.get('Symbol')}|Side:{data.get('Side')}{nl}|Price:{data.get('Price')}|Quantity:{data.get('Quantity')}|AccountID:{data.get('Account')}|ErrorCode:1{nl}|TimeStamp:{data.get('TimeStamp')}|Exchange_Order_Id:{ORDER_ID}|ChildResponseType:NULL_RESPONSE_MIDDLE{nl}|Duration:{data.get('Duration')}|ExchTs:{data.get('TimeStamp')}"
        
        filename = prefix + "trade_confirm.txt"
        file_path = "./outbound_messages/" + filename
        print("Generating TRADE_CONFIRM message")
        with open(file_path, "w") as f:
            f.write(converted)
            f.close()
        
        return converted

    def construct_new_order_confirm(self, data, prefix="") -> str:
        """This method constructs pipe delimited string for new order confirm message

        Args:
            data (dict): This is a parsed and converted exchange message data

        Returns:
            string: pipe demilited string message
        """
        nl = '\n'
        converted =  f"ResponseType:NEW_ORDER_CONFIRM|OrderID:{data['OrderID']}|Symbol:{data.get('Symbol')}|Side:{data.get('Side')}{nl}|Price:{data.get('Price')}|Quantity:{data.get('Quantity')}|AccountID:{data.get('Account')}|ErrorCode:1{nl}|TimeStamp:{data.get('TimeStamp')}|Exchange_Order_Id:{random.randint(10000,99999)}|ChildResponseType:NULL_RESPONSE_MIDDLE{nl}|Duration:{data.get('Duration')}|ExchTs:{data.get('TimeStamp')}"
        
        filename = prefix + "new_order_confirm.txt"
        file_path = "./outbound_messages/" + filename
        print("Generating NEW_ORDER_CONFIRM message")
    
        with open(file_path, "w") as f:
            f.write(converted)
            f.close()
        
        return converted
        
    def message_parser(self, data) -> list:
        """ This method applies the rules on provided dataset
        
        flag = 0 --> NEW_ORDER_CONFIRM
        flag = 1 --> REJECT
        tc_flag = 1 --> TRADE_CONFIRM 

        Args:
            data (dict): This is a parsed and converted exchange message data

        Returns:
            list: status value (0's, 1's)
        """
        
        flag, tc_flag = 0, 0
        self.generate_order_id()
        
        qty = int(data.get('Quantity'))
        # print(qty)
        
        sym = data.get('Symbol')
        # print(sym)
        
        price = float(data.get("Price"))
        # print(price)
        
        # If the qty of an order is multiple of x then generate NEW_ORDER_CONFIRM otherwise reject
        # x = 5
        if qty%5 != 0:
            print("Quantity rule failed")
            flag = 1

        # If the symbol is xyz then generate new_order_confirm and trade_confirm
        # x = 'BRN'    
        if 'BRN' not in sym:
            print("Symbol rule failed")
            flag = 1
        else:
            if price > 200:  # If price is greater than x=100 for symbol xyz then reject
                print("Symbol rule passed but Price rule failed")
                flag = 1
            tc_flag = 1
        if price == 123:  # If price is 123 then generate reject
            print("Price rule failed")
            flag = 1

        return [flag, tc_flag]

    def outbound_message(self, data, flag, prefix="") -> tuple:
        """This method triggers the outbound messages

        Args:
            flag (list of integer): [0, 1]

        Returns:
            tuple: constructed message
        """
        new_order_confirm, reject, trade_confirm = None, None, None
        if flag[0] == 0:
            new_order_confirm = self.construct_new_order_confirm(data, prefix)
        if flag[0] == 1:
            reject = self.construct_reject(data, prefix)
        if flag[0] !=1 and flag[1] == 1:
            trade_confirm = self.construct_trade_confirm(data, prefix)

        return new_order_confirm, trade_confirm, reject
        

if __name__ == '__main__':
    input_file_name = "IncomingMessage.txt"
    re = RuleEngine()
    data = re.read_message_from_textfile(input_file_name)  # here we are reading the input message from text file
    dict_data = re.convert_to_dict(data)  # here we are converting string data to dict data type
    status = re.message_parser(dict_data)  # here we are parsing the message data according to the given rule
    new_order_confirm, trade_confirm, reject = re.outbound_message(dict_data, status) # here we are constructing outbound messages
    print(new_order_confirm)
    print(trade_confirm)
