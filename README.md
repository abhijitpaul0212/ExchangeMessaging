# ExchangeMessaging

## Project Overview:

On a front office trading platform, one of the services would send order orders to exchange for
execution. Exchange may send a variety of responses to an order depending on various factors.
Automation is an essential part of SDLC and we would like to automate this flow such that exchange
behavior can be controlled and made predictable.

One possible way to control the exchange behavior is to implement a rule engine which can be used
to generate a specific kind of a response to a request matching a certain criterion.

The rules can be –
- If the qty of an order is multiple of x then generate NEW_ORDER_CONFIRM otherwise reject
- If the symbol is xyz then generate new_order_confirm and trade_confirm
- If price is greater than x for symbol xyz then reject
- If price is 123 then generate reject
- And so on..

We need you to implement an application which –
1. Receives the incoming requests
2. Parses the requests
3. Evaluates the configured rules
4. Send the response back as per the rule outcome. The rule can be configured to send more
than one response to a request.
The request/response may be sent/received over TCP or from file or shared memory. You are free to
choose the transport mechanism of your choice.
Also, write a script which compares the received responses with the responses stored in a golden
copy source. Any difference should be highlighted in a file/email or over console.

Sample request –
RequestType:NEWORDER|OrderID:480069891|Token:0|Symbol:IFEU_BRN
FMZ0022!|Side:B|Price:157.40000000000000568|Quantity:5|QuantityFilled:0|DisclosedQnty:5|Tim
eStamp:1666287639395048969|Duration:DAY|OrderType:LIMIT|Account:bJEROM
|Exchange:0|NumCopies:0


Possible responses -
ResponseType:NEW_ORDER_CONFIRM|OrderID:480069891|Symbol:IFEU_BRN
FMZ0022!|Side:B|Price:157.40000000000000568|Quantity:5|AccountID:bJEROM
|ErrorCode:1|TimeStamp:1666287639692625876|Exchange_Order_Id:13007294|ChildResponseTyp
e:NULL_RESPONSE_MIDDLE|Duration:DAY|ExchTs:1666287639962000000

ResponseType:TRADE_CONFIRM|OrderID:480069891|Symbol:IFEU_BRN
FMZ0022!|Side:B|Price:158.40000000000000568|Quantity:3|AccountID:bJEROM
|ErrorCode:1|TimeStamp:1666287790603407546|Exchange_Order_Id:13007306|ChildResponseTyp
e:NULL_RESPONSE_MIDDLE|Duration:DAY|ExchTs:1666287790989000000

ResponseType:REJECT|OrderID:480069891|Symbol:IFEU_BRN
FMZ0022!|Side:B|Price:158.40000000000000568|Quantity:4|AccountID:bJEROM
|ErrorCode:100109|TimeStamp:1666287933899054797|Exchange_Order_Id:0|ChildResponseType:
CANCEL_ORDER_REJECT_MIDDLE|Duration:DAY|ExchTs:0


## Assumptions:

1. Inbound message to the exchange is provided in .txt files
2. Valid quantity is 5 and its multiples only
3. Valid symbol is having 'BRN' in it
4. Valid price is < 200 if above symbol matches
5. Irrespective of symbol, if price is nbot equal to 123


## Design Decision

1. We will read the inbound message from given .txt file
2. Once data is read, its converted into a dictionary dataset for better usage throughout the project
3. We will create a parser method, who's purpose will be to parse each key-value pair from the dictionary dataset and than validate it as per the given rules.
4. Once validated, we will construct appropriate outbound messages as per requirements.
5. We will share the outbound messages in the console and at the same time we will generate .txt file as well for further usages.

#### Out of Scope:

1. Anything other then the above design decision is not within the scope of this project
