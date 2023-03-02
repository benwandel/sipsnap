# sipsnap
automation for mcdonald´s feedback system

browser settings:
maybe the browser setup settings have to be changed, depending on the browser which should be used for the processing the poll.
you can find these settings in line 20.

necessary changes in code:

'options.binary_location' in line 22: 
path to .exe of used browser

'accepted_button.send_keys' in line 301: 
path to receipt of mcdonald´s receipt (only german receipts will work)

'openai.api_key' in line 406:
OpenAI API Key for a automated answer from ChatGPT

'complete_name_qr' in line 500 AND 'os.remove' in line 510:
path to store the qr code -> where to store the .png of the qr code for free drink

'complete_name_code' in line 501 AND 'os.remove' in line 511:
path to store the voucher code -> where to store the .txt of the voucher code for free drink
