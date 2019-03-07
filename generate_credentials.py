from PyInquirer import style_from_dict, Token, prompt, Separator
import argparse, requests, sys

# Device types
device_types = ['papa-duck', 'android']
help_str_device_types = "either "
for d in device_types:
  help_str_device_types += '{d} or '.format(d=d)
help_str_device_types = help_str_device_types[:-4]
parser = argparse.ArgumentParser(
  description='Create a duck and generate a credentials.h file.'+ 
  'Leave parameters blank for an interactive prompt.'
)
parser.add_argument('--device_type',
                    help='The device type, {hs}'.format(hs=help_str_device_types))
parser.add_argument('--device_id',
                    help='The device ID. MAC Address or other unique identifier')
args = parser.parse_args()

# Server base URL
base_url = 'https://ducks-to-db.mybluemix.net'

style = style_from_dict({
  Token.Separator: '#cc5454',
  Token.QuestionMark: '#673ab7 bold',
  Token.Selected: '#cc5454',  # default
  Token.Pointer: '#673ab7 bold',
  Token.Instruction: '',  # default
  Token.Answer: '#f44336 bold',
  Token.Question: '',
})

questions = [
  {
    'type': 'list',
    'message': 'What is the device type?',
    'name': 'device_type',
    'choices': device_types
  },
  {
    'type': 'input',
    'message': 'What is the device ID?',
    'name': 'device_id',
    'validate': lambda answer: 'You must specify a device ID' \
        if len(answer) == 0 else True
  }
]

if args.device_type and args.device_id:
  device_type = args.device_type
  device_id = args.device_id

  if device_type not in device_types:
    sys.exit("Please specify a valid device type, {hs}"
      .format(hs=help_str_device_types))
else:
  answers = prompt(questions, style=style)
  device_type = answers['device_type']
  device_id = answers['device_id']

print('🦆 OK! Great.. Setting up a new {device_type} device with ID: {device_id}'
  .format(device_type=device_type, device_id=device_id))
print('🦆 .......')

# Call to API to register new device
post_obj = {"type": device_type, "id": device_id}
url = base_url +'/api/devices'
r = requests.post(url, json=post_obj)

if (r.status_code == 200):
  print('🦆 Created a new {device_type} in IBM Watson IoT and Postgres.'
    .format(device_type=device_type))
  
  file_str = r.json()['file']
  with open('./credentials.h', "w") as creds_file:
    creds_file.write(file_str)

  print('🦆 credentials.h file created!')

else:
  print('🦆 Oh no! There has been an error creating the device:')
  print(r)
