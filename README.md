# sipsnap
automation for users in mcdonald´s feedback system

description:
this is a code for automatically processing the mcdonald´s feedback poll of germany. for trying out this code you need to do some changes of different variables. it is explained in detail in the next lines.

browser settings:
maybe the browser setup settings have to be changed, depending on the browser which should be used for the processing the poll.
you can find these settings in line 20.

necessary changes in code:

'options.binary_location' in line 22: 
path to .exe of used browser

'accepted_button.send_keys' in line 301: 
path to receipt of mcdonald´s receipt (only german receipts will work)

'openai.api_key' in line 406:
openai api key for a automated answer from chatgpt

'path_store_voucher' in line 494:
path to store the qr code and voucher code for the free drink
