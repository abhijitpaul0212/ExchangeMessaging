import unittest
from rule_engine import RuleEngine


class TestRuleEngine(unittest.TestCase):
    """
    This class contains the Test Cases for Rule Engine
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.re = RuleEngine()
        cls.filename = "IncomingMessage.txt"

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self) -> None:
        # Read the input message from text file
        self.data = self.re.read_message_from_textfile(self.filename)

        # Convert the input message into dictionary data type
        self.data_dict = self.re.convert_to_dict(self.data)

    def tearDown(self) -> None:
        pass

    def test_valid_message(self):
        status = self.re.message_parser(self.data_dict)
        self.assertEqual(status, [0, 1], "Verifying NEW_ORDER_CONFIRM & TRADE_CONFIRM message got generated")
        new_order_confirm, trade_confirm, reject = self.re.outbound_message(self.data_dict, status, prefix="valid")
        o_new_order_confirm = self.re.convert_to_dict(new_order_confirm)
        self.assertEqual(o_new_order_confirm.get('ResponseType'), "NEW_ORDER_CONFIRM", "Verifying ResponseType tag")
        self.assertEqual(int(o_new_order_confirm.get('Quantity')) % 5 == 0, True, "Verifying Quantity tag")
        self.assertEqual('BRN' in o_new_order_confirm.get('Symbol'), True, "Verifying Symbol tag")
        self.assertEqual(float(o_new_order_confirm.get('Price')) < 200, True, "Verifying Price tag")

        o_trade_confirm = self.re.convert_to_dict(trade_confirm)
        self.assertEqual(o_trade_confirm.get('ResponseType'), "TRADE_CONFIRM", "Verifying ResponseType tag")
        self.assertEqual(int(o_trade_confirm.get('Quantity')) % 5 == 0, True, "Verifying Quantity tag")
        self.assertEqual('BRN' in o_trade_confirm.get('Symbol'), True, "Verifying Symbol tag")
        self.assertEqual(float(o_trade_confirm.get('Price')) < 200, True, "Verifying Price tag")

    def test_invalid_quantity(self):
        self.data_dict["Quantity"] = 7  # invalid quantity
        status = self.re.message_parser(self.data_dict)
        self.assertEqual(status[0], 1, "Verifying REJECT message got generated")
        new_order_confirm, trade_confirm, reject = self.re.outbound_message(self.data_dict, status,
                                                                            prefix="invalid")
        o_new_order_confirm = self.re.convert_to_dict(reject)
        self.assertEqual(o_new_order_confirm.get('ResponseType'), "REJECT", "Verifying ResponseType tag")
        self.assertEqual(int(o_new_order_confirm.get('Quantity')) % 5 == 0, False, "Verifying Quantity tag")


    def test_invalid_symbol(self):
        self.data_dict["Symbol"] = "IFEU_XRNFMZ0022!"  # invalid symbol
        status = self.re.message_parser(self.data_dict)
        self.assertEqual(status[0], 1, "Verifying REJECT message got generated")
        new_order_confirm, trade_confirm, reject = self.re.outbound_message(self.data_dict, status,
                                                                            prefix="invalid")
        o_new_order_confirm = self.re.convert_to_dict(reject)
        self.assertEqual(o_new_order_confirm.get('ResponseType'), "REJECT", "Verifying ResponseType tag")
        self.assertEqual("BRN" in (o_new_order_confirm.get('Symbol')), False, "Verifying Symbol tag")

    def test_valid_symbol_invalid_price(self):
        self.data_dict["Price"] = "250.9000129"  # invalid Price
        status = self.re.message_parser(self.data_dict)
        self.assertEqual(status[0], 1, "Verifying REJECT message got generated")
        new_order_confirm, trade_confirm, reject = self.re.outbound_message(self.data_dict, status,
                                                                            prefix="invalid")
        o_new_order_confirm = self.re.convert_to_dict(reject)
        self.assertEqual(o_new_order_confirm.get('ResponseType'), "REJECT", "Verifying ResponseType tag")
        self.assertEqual(float(o_new_order_confirm.get('Price')) > 200, True, "Verifying Price tag")

    def test_invalid_price(self):
        self.data_dict["Price"] = "123"  # invalid Price
        status = self.re.message_parser(self.data_dict)
        self.assertEqual(status[0], 1, "Verifying REJECT message got generated")
        new_order_confirm, trade_confirm, reject = self.re.outbound_message(self.data_dict, status,
                                                                            prefix="invalid")
        o_new_order_confirm = self.re.convert_to_dict(reject)
        self.assertEqual(o_new_order_confirm.get('ResponseType'), "REJECT", "Verifying ResponseType tag")
        self.assertEqual(float(o_new_order_confirm.get('Price')) == 123, True, "Verifying Price tag")
